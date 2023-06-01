import time
import random
import string
from conf.configs import instance_att, tags


def camel_to_underline(camel_str):
    """
    将驼峰格式字符串转换为下划线格式字符串（特定字符串 'CPU' 转换为小写字母）
    """
    if camel_str == 'CPU':
        return 'cpu'
    if 'CPU' in camel_str:
        camel_str = camel_str.replace('CPU', 'Cpu')
    res = ''
    for i, s in enumerate(camel_str):
        if s.islower():
            res += s
        elif s.isupper():
            if i > 0 and camel_str[i-1:i+1].islower():
                res += '_' + s.lower()
            else:
                res += '_' + s.lower()
        else:
            res += '_'
    return res.lstrip('_')


def merge_dict(dict1, dict2):
    for k, v in dict2.items():
        dict1[k] = v
    return dict1


def get_tags(tag):
    tags_dict = {}
    for tag in tag:
        tags_dict[tag["TagKey"]] = tag["TagValue"]
    return tags_dict


def get_tags_kv(tag):
    tags_dict = {}
    for tag in tag:
        tags_dict[tag["Key"]] = tag["Value"]
    return tags_dict


def get_lbs():
    return instance_att + tags


def get_instance_lb(instance_info):
    lb_list = [instance_info.get(key, '') for key in instance_att]
    lb_list += [instance_info['tags'].get(key, '') for key in tags]
    return lb_list


def retry(tries=3, interval=1):
    # 装饰器，任务函数调用时，进行重试三次
    def decorate(func):
        def wrapper(*args, **kwargs):
            count = 0
            while True:
                try:
                    result = func(*args, **kwargs)
                except Exception as e:
                    count += 1
                    if count > tries:
                        break
                    else:
                        print("retry count is %s, metric_name is %s , %s" % (count, args[1], e))
                        time.sleep(interval)
                else:
                    return result
        return wrapper
    return decorate


def generate_random_string(length):
    """
    生成指定长度的随机字母数字字符串
    """
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))
