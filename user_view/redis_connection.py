import redis
import os

# client = redis.Redis(host='localhost', port=6379, db=0)
r = redis.Redis(
  host=os.getenv('host'),
  port=os.getenv('port'),
  password=os.getenv('password')
)




