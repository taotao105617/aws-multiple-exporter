import time
import threading
from conf.configs import cache_invalidation_time


def cache_product(product):
    if product == 'redis':
        from service.aws_redis.aws_redis_svc import AwsRedisSvc
        aws_redis_svc = AwsRedisSvc()
        start_cache_job(aws_redis_svc.get_redis_cache)


def start_cache_job(func):
    t = threading.Thread(target=cache_job, args=(func,))
    t.start()


def cache_job(func, s=cache_invalidation_time):
    # 执行传入的函数，并传递一个字符串参数
    while True:
        func()
        time.sleep(s-90)
