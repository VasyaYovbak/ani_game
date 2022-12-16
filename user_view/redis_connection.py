import redis
# from datetime import timedelta, datetime, timezone
#
jwt_redis_blacklist = redis.Redis(
    host="localhost", port=6379, db=0, decode_responses=True
)
# jti = 'sdawdasdawdasdawd'
# ACCESS_EXPIRES = timedelta(days=1)
#
#
# print(jwt_redis_blacklist.set(name="jti", value=jti, ex=ACCESS_EXPIRES))
# print(str(jwt_redis_blacklist.get('jti')))
#
# access_token_lifetime = datetime.fromtimestamp(1660929512)
# print(access_token_lifetime)
#
# jwt_redis_blacklist.close()
