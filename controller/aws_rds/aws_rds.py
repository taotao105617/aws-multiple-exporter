from prometheus_client.core import GaugeMetricFamily
from lib.tool import get_lbs, get_instance_lb


def aws_rds_exporter(aws_instance_infos):
    aws_rds_disk_allocated_storage = GaugeMetricFamily('aws_rds_disk_allocated_storage', 'DESC: 磁盘容量 unit: GB',
                                                       labels=get_lbs())
    generates_spec = {
        'aws_rds_disk_allocated_storage': {
            'prom_metric_gauge': aws_rds_disk_allocated_storage,
        }
    }
    for account, region_instance_info in aws_instance_infos.items():
        for region, instance_infos in region_instance_info.items():
            for instance, instance_info in instance_infos.items():
                allocated_storage = instance_info.get('allocated_storage')
                if allocated_storage == 1:
                    continue
                aws_rds_disk_allocated_storage.add_metric(get_instance_lb(instance_info), allocated_storage)
    return generates_spec

