import redis
import os

# client = redis.Redis(host='localhost', port=6379, db=0)
r = redis.Redis(
  host=os.getenv('REDIS_HOST'),
  port=int(os.getenv('REDIS_PORT')),
  password=os.getenv('REDIS_PASSWORD')
)




