from models.aws_redis.aws_redis_info import AwsRedis
from models.aws_account.aws_account import get_account_info
from lib.redis_client import r
from lib.aws_client import get_client
from lib.logger import logs
from conf.configs import cache_invalidation_time


class AwsRedisSvc:
    def __init__(self):
        pass

    def get_all_aws_redis_instances(self):
        # 获取所有账号信息
        all_redis = {}
        aws_accounts = get_account_info()
        for account, aws_account in aws_accounts.items():
            regions = aws_account['regions']
            ak = aws_account['ak']
            sk = aws_account['sk']
            redis_obj = AwsRedis(ak=ak, sk=sk, regions=regions)
            account_aws_redis_instances = redis_obj.get_account_aws_redis_instances(account)
            all_redis[account] = account_aws_redis_instances
        return all_redis

    def cache_all_aws_redis_instances(self):
        aws_redis_infos = self.get_all_aws_redis_instances()
        r.set('aws_redis_infos', str(aws_redis_infos), ex=cache_invalidation_time)

    def get_redis_cache(self):
        aws_redis_infos = r.get('aws_redis_infos')
        if aws_redis_infos is None:
            # 重新加载缓存
            logs.info('reset aws redis instance cache')
            self.cache_all_aws_redis_instances()
        aws_redis_infos = r.get('aws_redis_infos')
        return eval(aws_redis_infos)

    def get_monitor_data(self, account, region, mqs, start_time, end_time, monitor_queue):
        monitor_data = []
        account_info_dict = get_account_info()
        ak = account_info_dict[account]['ak']
        sk = account_info_dict[account]['sk']

        cloudwatch = get_client(ak, sk, 'cloudwatch', region)
        response = cloudwatch.get_metric_data(
            MetricDataQueries=mqs,
            StartTime=start_time,
            EndTime=end_time,
        )
        for result in response['MetricDataResults']:
            res_lb = result['Label'].split(' ')
            instance = res_lb[0]
            metrics_name = res_lb[1]
            if 'Values' in result:
                values = result['Values']
                if len(values) > 0:
                    value = values[0]
                    monitor_data.append({
                        'instance': instance,
                        'metrics_name': metrics_name,
                        'value': value,
                        'account': account,
                        'region': region
                    })
        monitor_queue.put(monitor_data)
        return monitor_data




