from conf.configs import configs


def get_account_info():
    aws_account_infos = configs.get('aws_account_infos')
    account_dict = {}
    for i, aws_account_info in enumerate(aws_account_infos):
        account = aws_account_info['account']
        regions = aws_account_info['regions']
        if not isinstance(regions, list):
            regions = regions.split(',')
        aws_account_infos[i]['regions'] = regions
        account_dict[account] = aws_account_infos[i]
    return account_dict

