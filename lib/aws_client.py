import boto3
from lib.tool import generate_random_string


def get_client(ak, sk, namespace, region):
    # 设置AWS凭证认证信息
    session = boto3.Session(
        aws_access_key_id=ak,
        aws_secret_access_key=sk,
        region_name=region
    )

    # 创建CloudWatch客户端
    client = session.client(namespace)
    return client


def metric_data_queries(aws_instance_infos, namespace, instance_type, generates):
    # aws_redis_infos --> {'account': {'region': {'instance': {xxx}}}}
    # 按照账号、区域维度生成 mqs，mqs内包含不同实例的不同指标 max 500个
    # mqs_dict # {"account": {"region": []}}
    mqs_dict = {}

    for account, region_instances in aws_instance_infos.items():
        for region, instances in region_instances.items():
            mqs = []
            for instance in instances:
                for metric_name, prom_gauge_info in generates.items():
                    statistics = prom_gauge_info['statistics']
                    mq = {
                        'Id': 'id%s' % generate_random_string(8),
                        'MetricStat': {
                            'Metric': {
                                'Namespace': namespace,
                                'MetricName': metric_name,
                                'Dimensions': [
                                    {
                                        'Name': instance_type,
                                        'Value': instance
                                    }
                                ]
                            },
                            'Period': 60,
                            'Stat': statistics,
                        }
                    }
                    if mqs_dict.get(account) is None:
                        mqs_dict[account] = {}
                    if mqs_dict[account].get(region) is None:
                        mqs_dict[account][region] = []
                    if len(mqs) == 500:
                        mqs_dict[account][region].append(mqs)
                        mqs = []
                    mqs.append(mq)
            mqs_dict[account][region].append(mqs)
        return mqs_dict
