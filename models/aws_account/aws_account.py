from conf.configs import aws_account_infos


def get_account_info():
    account_dict = {}
    for i, aws_account_info in enumerate(aws_account_infos):
        account = aws_account_info['account']
        regions = aws_account_info['regions']
        if not isinstance(regions, list):
            regions = regions.split(',')
        aws_account_infos[i]['regions'] = regions
        account_dict[account] = aws_account_infos[i]
    return account_dict

