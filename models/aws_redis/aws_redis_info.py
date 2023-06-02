import threading
import queue
from lib.aws_client import get_client
from lib.tool import get_tags_kv, merge_dict


class AwsRedis:
    def __init__(self, ak, sk, regions):
        self.regions = regions
        self.ak = ak
        self.sk = sk
        self.namespace = 'elasticache'

    def get_one_aws_redis_tags(self, client, cache_cluster_arn):
        response = client.list_tags_for_resource(ResourceName=cache_cluster_arn)
        tags = get_tags_kv(response['TagList'])
        return tags

    def get_region_aws_redis_instances(self, result_queue, region, account):
        client = get_client(self.ak, self.sk, self.namespace, region)
        aws_redis = {region: {}}
        response = client.describe_cache_clusters()
        # 循环遍历每个 Redis 实例
        for cache_cluster in response['CacheClusters']:
            if cache_cluster['Engine'] != 'redis':
                continue
            # 获取当前实例的 ID 和 ARN
            cache_cluster_id = cache_cluster['CacheClusterId']
            cache_cluster_arn = cache_cluster['ARN']
            engine_version = cache_cluster['EngineVersion'],
            zone = cache_cluster['PreferredAvailabilityZone']
            tags = self.get_one_aws_redis_tags(client, cache_cluster_arn)
            aws_redis[region][cache_cluster_id] = {
                'tags': tags,
                'region': region,
                'instance': cache_cluster_id,
                'engine_version': engine_version,
                'zone': zone,
                'account': account
            }
        # 数据推送至
        result_queue.put(aws_redis)
        return aws_redis

    # def get_account_aws_redis_instances(self, account):
    #     redis_account = {}
    #     threads = []
    #     # 创建消息队列
    #     result_queue = queue.Queue()
    #     for region in self.regions:
    #         # aws_client = get_client(self.ak, self.sk, self.namespace, region)
    #         # redis_region = self.get_region_aws_redis_instances(aws_client, region)
    #         # redis_account[region] = redis_region
    #         t = threading.Thread(target=self.get_region_aws_redis_instances, args=(result_queue, region, account))
    #         threads.append(t)
    #         t.start()
    #     # 等待所有线程完成
    #     for t in threads:
    #         t.join()
    #     # 获取计算结果
    #     while not result_queue.empty():
    #         # 合并数据
    #         redis_account = merge_dict(redis_account, result_queue.get())
    #     return redis_account



