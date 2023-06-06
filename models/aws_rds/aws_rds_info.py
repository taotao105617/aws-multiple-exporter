from lib.aws_client import get_client


class AwsRds:
    def __init__(self, ak, sk, regions):
        self.regions = regions
        self.ak = ak
        self.sk = sk
        self.namespace = 'rds'

    def tags_list2dict(self, tags_list):
        return {tag['Key']: tag['Value'] for tag in tags_list}

    def get_region_aws_rds_instances(self, result_queue, region, account):
        aws_rds = {region: {}}
        # get all rds
        rds_client = get_client(self.ak, self.sk, self.namespace, region)
        rds_instances = rds_client.describe_db_instances()
        for instance_info in rds_instances['DBInstances']:
            tags = instance_info['TagList']
            host = instance_info['Endpoint']['Address']
            port = instance_info['Endpoint']['Port']
            zone = instance_info['AvailabilityZone']
            instance = instance_info['DBInstanceIdentifier']
            allocated_storage = instance_info['AllocatedStorage']
            aws_rds[region][instance] = {
                'tags': self.tags_list2dict(tags),
                'host': host,
                'port': port,
                'region': region,
                'zone': zone,
                'instance': instance,
                'account': account,
                'allocated_storage': allocated_storage
            }
        # 推送数据到消息队列
        result_queue.put(aws_rds)
        return aws_rds

