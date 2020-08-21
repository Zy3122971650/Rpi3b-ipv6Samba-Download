import redis

r = redis.Redis(port=10086,decode_responses=True)
r.lpush('list1','22','33')

print(r.keys())
print(r.lrange('list1',0,-1))
