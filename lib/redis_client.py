import redis
from conf.configs import configs

redis_configs = configs.get('redis_configs')

# redis client
r = redis.Redis(host=redis_configs['redis_address'], port=redis_configs['redis_ports'], decode_responses=True,
                password=redis_configs['redis_password'])
