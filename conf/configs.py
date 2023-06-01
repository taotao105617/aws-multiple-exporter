logs_dir = './logs'
# 环境
env = 'online'
# 启动端口
address_ports = {
    'redis': 8888
}
# redis 配置
redis_address = '127.0.0.1'
redis_ports = 6379
redis_password = None
cache_invalidation_time = 1000


# exporter 标签
instance_att = ['host', 'instance', 'port', 'account', 'region']
tags = ['app', 'app_id', 'cloud', 'cloud_name', 'env', 'port', 'projname', 'type']

# aws 云产品 命名空间和过滤条件
ProductNamespaceF = {
    'redis': {
        'namespace': 'AWS/ElastiCache',
        'filter': 'CacheClusterId'
    }
}

# aws 账号信息
aws_account_infos = [
    {
        'account': 'xxx',
        'ak': 'xxxx',
        'sk': 'xxxx',
        'regions': 'us-east-1,ap-southeast-1,eu-central-1,sa-east-1'
    }
]




