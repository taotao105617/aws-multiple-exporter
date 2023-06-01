import redis
from conf.configs import redis_address, redis_ports, redis_password

# redis client
r = redis.Redis(host=redis_address, port=redis_ports, decode_responses=True, password=redis_password)
