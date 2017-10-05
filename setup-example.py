import redis

FirstURL = "https://en.wikipedia.org/wiki/List_of_blogs"

r = redis.Redis(
    host='localhost',
    port=6379)

if not r.get('firstKey'):
    r.set('firstKey', 0)
    print('Set the firstKey to 0')

if not r.get('lastKey'):
    r.set('lastKey', 1)
    print('Set the lastKey to 1')

firstKey = int(r.get('firstKey'))
r.set(firstKey,FirstURL)
