import requests
import json
import slugify
from redis_util import redis_get, city_key

destinations = []


def load_destinations():
    url = "https://www.studentagency.cz/data/wc/ybus-form/destinations-sk.json"
    return requests.get(url).json()


def load_cities():
    global destinations
    if not destinations:
        destinations = load_destinations()
        destinations = destinations["destinations"]

    cities_by_countries = list(map(lambda country: country["cities"], destinations))
    return [city for cities in cities_by_countries for city in cities]


def get_city_by_name(city_name, cities):
    for city in cities:
        if slugify.slugify(city_name).lower() in slugify.slugify(city["name"]).lower():
            return city


def get_city_by_id(city_id, cities):
    for city in cities:
        if city_id == city["id"]:
            return city


def get_location_id(city_name, cities):
    key = city_key(city_name)

    kwargs = {"city_name": city_name, "cities": cities}
    city = redis_get(key, 60 * 60, get_city_by_name, kwargs)

    if not city:
        return None

    return city["id"]


def get_city_name(city_id, cities):
    city = get_city_by_id(city_id, cities)
    return city["name"]
