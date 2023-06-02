import queue
import threading
import time
from datetime import datetime, timedelta
from prometheus_client.core import GaugeMetricFamily
from prometheus_client import Counter
from service.aws_svc import AwsSvc
from lib.yaml_reader import YamlReader
from lib.tool import camel_to_underline, get_lbs, get_instance_lb
from lib.aws_client import metric_data_queries
from lib.logger import logs
from conf.configs import ProductNamespaceF


# 计算调用cloudwatch次数，可用于评估费用
aws_cloudwatch_request = Counter('aws_cloudwatch_request_count', 'DESC: 调用cloudwatch次数 unit: count', ['product'])
# 计算调用cloudwatch指标总数

aws_cloudwatch_metric_request = Counter('aws_cloudwatch_metric_request_count', 'DESC: 调用cloudwatch 指标总数 unit: '
                                                                               'count', ['product'])


class AwsCollector(object):
    def __init__(self, product):
        self.product = product

    def generate_metrics(self):
        generates = {}
        yaml_file = self.product + '.yaml'
        yaml_reader = YamlReader(yaml_file)
        metrics = yaml_reader.read()

        for metric in metrics['task']:
            namespace = metric['namespace']
            metrics = metric['metrics']
            for metric_info in metrics:
                metric_name = metric_info['metric_name']
                statistics = metric_info['statistics']
                prom_name = 'aws_' + namespace + '_' + camel_to_underline(metric_name) + '_' + \
                            camel_to_underline(statistics)
                metric_desc = metric.get('metric_desc', '')
                prom_metric_gauge = GaugeMetricFamily(prom_name, metric_desc, labels=get_lbs())
                generates[metric_name] = {
                    'prom_metric_gauge': prom_metric_gauge,
                    'statistics': statistics
                }
                logs.info("generate metrics %s" % prom_name)
        return generates

    def get_product_instance_info(self):
        # 获取所有账号实例信息（cache）
        svc = AwsSvc(self.product)
        aws_instance_infos = svc.get_cache()
        return svc, aws_instance_infos

    def aws_exporter_monitor_data(self, generates, aws_instance_infos, aws_svc):
        monitor_data_list = []
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(minutes=6)

        # 组装cloudwatch需要的mqs
        mqs_dict = metric_data_queries(aws_instance_infos, ProductNamespaceF[self.product]['namespace'],
                                       ProductNamespaceF[self.product]['filter'], generates)

        # 创建消息队列
        monitor_queue = queue.Queue()
        threads = []
        num = 0
        for account, redis_regions in mqs_dict.items():
            for region, mqs_list in redis_regions.items():
                for mqs in mqs_list:
                    num += 1
                    aws_cloudwatch_request.labels(product=self.product).inc()
                    aws_cloudwatch_metric_request.labels(product=self.product).inc(len(mqs))
                    # 多线程获取监控数据
                    t = threading.Thread(target=aws_svc.get_monitor_data, args=(account, region, mqs, start_time,
                                                                                end_time, monitor_queue))
                    threads.append(t)
                    t.start()
                    # 每10个线程等待1s
                    if num % 10 == 0:
                        time.sleep(1)

        # 等待所有线程完成
        for t in threads:
            t.join()
        # 获取线程结果
        while not monitor_queue.empty():
            # 合并数据
            monitor_data_list += monitor_queue.get()
        return monitor_data_list

    def collect(self):
        # 生成prometheus gauge对象
        generates = self.generate_metrics()
        # 获取所有账号实例信息（cache）
        svc = self.get_product_instance_info()
        aws_instance_infos = svc[1]
        aws_svc = svc[0]
        # 获取监控数据
        monitor_data_list = self.aws_exporter_monitor_data(generates, aws_instance_infos, aws_svc)
        # 根据返回结果和prometheus对象对应关系上报数据
        for monitor_data in monitor_data_list:
            instance = monitor_data['instance']
            account = monitor_data['account']
            region = monitor_data['region']
            metric_name = monitor_data['metrics_name']
            value = monitor_data['value']

            instance_info = aws_instance_infos[account][region][instance]
            instance_labels = get_instance_lb(instance_info)

            prom_gauge = generates[metric_name]['prom_metric_gauge']
            prom_gauge.add_metric(instance_labels, value)
        # yield prometheus 对象
        for metric_name, prom_gauge_info in generates.items():
            yield_prom_gauge = prom_gauge_info['prom_metric_gauge']
            yield yield_prom_gauge
