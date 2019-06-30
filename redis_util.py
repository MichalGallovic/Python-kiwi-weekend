from redis import StrictRedis
import slugify
import json

redis = None


def get_redis():
    global redis
    if not redis:
        with open("redis.json", "r") as file:
            redis_config = json.load(file)
        redis = StrictRedis(socket_connect_timeout=3, **redis_config)
    return redis


def redis_get(key, expiration, closure, kwargs):
    redis = get_redis()

    if not redis:
        return closure(**kwargs)

    if not redis.exists(key):
        output = closure(**kwargs)
        redis.setex(key, expiration, json.dumps(output))
        return output

    return json.loads(redis.get(key))


def journey_key(source, destination, departure_date):
    source = slugify.slugify(source)
    destination = slugify.slugify(destination)
    departure_date = slugify.slugify(departure_date)
    return f"4242:journey:{source}_{destination}_{departure_date}_studentagency"


def city_key(location_name):
    return f"4242:location:{slugify.slugify(location_name)}_studentagency"


def journey_key(source, destination, departure_date):
    source = slugify.slugify(source)
    destination = slugify.slugify(destination)
    departure_date = slugify.slugify(departure_date)
    return f"4242:journey:{source}_{destination}_{departure_date}_studentagency"
