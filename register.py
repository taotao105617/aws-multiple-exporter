import time
import threading
from conf.configs import cache_invalidation_time
from service.aws_svc import AwsSvc


def cache_product(product):
    aws_svc = AwsSvc(product)
    start_cache_job(aws_svc.get_cache)


def start_cache_job(func):
    t = threading.Thread(target=cache_job, args=(func,))
    t.start()


def cache_job(func, s=cache_invalidation_time):
    # 执行传入的函数，并传递一个字符串参数
    while True:
        func()
        time.sleep(s-90)
