import threading
import queue
from lib.tool import merge_dict
import models.aws_redis.aws_redis_info as awsRedis
import models.aws_rds.aws_rds_info as awsRds


class_dict = {
    'redis': awsRedis,
    'rds': awsRds
}


def get_account_aws_instances(ak, sk, regions, account, product):
    product_capitalize = product.capitalize()
    # 组装类名称
    product_class_name = 'Aws' + product_capitalize
    # 生成类
    generate_class = getattr(class_dict[product], product_class_name)
    # 实例化类
    product_class = generate_class(ak, sk, regions)
    # 产品函数名称
    generate_func = 'get_region_aws_%s_instances' % product
    # 生成函数
    product_func = getattr(product_class, generate_func)

    account_instances = {}
    threads = []
    # 创建消息队列
    result_queue = queue.Queue()
    for region in regions:
        # aws_client = get_client(ak, sk, ProductNamespaceF[product]['namespace'], region)
        t = threading.Thread(target=product_func, args=(result_queue, region, account))
        threads.append(t)
        t.start()
    # 等待所有线程完成
    for t in threads:
        t.join()
    # 获取计算结果
    while not result_queue.empty():
        # 合并数据
        account_instances = merge_dict(account_instances, result_queue.get())
    return account_instances
