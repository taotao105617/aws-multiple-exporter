from lib.yaml_reader import YamlReader

logs_dir = './logs'

cache_invalidation_time = 1000


# exporter 标签
instance_att = ['host', 'instance', 'port', 'account', 'region']
tags = ['app', 'app_id', 'cloud', 'cloud_name', 'env', 'port', 'projname', 'type']

# aws 云产品 命名空间和过滤条件
ProductNamespaceF = {
    'redis': {
        'namespace': 'AWS/ElastiCache',
        'filter': 'CacheClusterId'
    },
    'rds': {
        'namespace': 'AWS/RDS',
        'filter': 'DBInstanceIdentifier'
    },
}


class Configs:
    def __init__(self):
        self.yaml_reader = YamlReader(file='configs.yaml', path='conf/')

    def get(self, key):
        data = self.yaml_reader.read()
        return data.get(key)


configs = Configs()
