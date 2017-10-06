import redis

FirstURL = "https://www.darknet.org.uk"

r = redis.Redis(
    host='localhost',
    port=6379)

r.set('firstKey', 0)
print('Set the firstKey to 0')

r.set('lastKey', 1)
print('Set the lastKey to 1')

firstKey = int(r.get('firstKey'))
r.set(firstKey,FirstURL)
