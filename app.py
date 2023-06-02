import time
import sys
from prometheus_client import start_http_server
from register import cache_product
from conf.configs import configs
from lib.logger import logs
from controller.prom_collect import AwsCollector
from prometheus_client.core import REGISTRY

address_ports = configs.get('address_ports')
env = configs.get('env')


def help():
    print('请输入正确的云产品')
    print('支持的产品列表 %s' % address_ports.keys())
    print('如: python3 app.py redis')
    sys.exit(1)


if __name__ == '__main__':
    if env != 'dev':
        args = sys.argv
        if len(args) != 2:
            help()
        product = args[1]
    else:
        product = 'redis'
    if product not in address_ports.keys():
        help()
    try:
        cache_product(product)
    except Exception as e:
        raise e
    start_http_server(address_ports[product])
    logs.info("http://127.0.0.1:%s" % address_ports[product])
    REGISTRY.register(AwsCollector(product))
    while True:
        time.sleep(0.01)
