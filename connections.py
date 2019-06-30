import json
import requests
from redis_util import redis_get, journey_key
from locations import (
    load_cities,
    get_city_name,
    get_location_id,
    get_city_by_id,
    get_city_by_name,
)
import hashlib


def connection_hash(connection):
    return hashlib.md5(
        f"{connection['arrival_datetime']}{connection['departure_datetime']}{connection['destination']}".encode(
            "utf-8"
        )
    ).hexdigest()


def fetch_connections(source, destination, departure_date):
    cities = load_cities()
    source_id = get_location_id(source, cities)
    destination_id = get_location_id(destination, cities)

    if not source_id or not destination_id:
        return []

    url = "https://brn-ybus-pubapi.sa.cz/restapi/routes/search/simple"
    response = requests.get(
        url,
        params={
            "locale": "sk",
            "departureDate": departure_date,
            "fromLocationId": source_id,
            "toLocationId": destination_id,
            "fromLocationType": "CITY",
            "toLocationType": "CITY",
            "tariffs": "REGULAR",
        },
    )
    response = response.json()

    if "routes" in response:
        routes = response["routes"]
        for i, route in enumerate(routes):
            routes[i]["source_city"] = get_city_name(source_id, cities)
            routes[i]["destination_city"] = get_city_name(destination_id, cities)
        return routes
    else:
        return []


def get_connections(source, destination, departure_date):
    key = journey_key(source, destination, departure_date)
    kwargs = {
        "source": source,
        "destination": destination,
        "departure_date": departure_date,
    }
    return redis_get(key, 60 * 60, fetch_connections, kwargs)
