import datetime
from locations import load_cities


def parse_stations(cities):
    return {
        station["id"]: station["fullname"]
        for city in cities
        for station in city["stations"]
    }


def format_datetime(string_datetime):
    return datetime.datetime.strptime(
        string_datetime, "%Y-%m-%dT%H:%M:%S.%f%z"
    ).strftime("%Y-%m-%d %H:%M:%S")


def format_connections(connections):
    cities = load_cities()
    stations = parse_stations(cities)
    formatted_connections = []
    for connection in connections:
        source_station_id = connection["arrivalStationId"]
        destination_station_id = connection["departureStationId"]
        formatted_connections.append(
            {
                "departure_datetime": format_datetime(connection["departureTime"]),
                "arrival_datetime": format_datetime(connection["arrivalTime"]),
                "source": stations[source_station_id],
                "destination": stations[destination_station_id],
                "source_city": connection["source_city"],
                "destination_city": connection["destination_city"],
                "price": connection["priceFrom"],
                "type": connection["vehicleTypes"],
                "free_seats": connection["freeSeatsCount"],
                "carrier": "studentagency",
                "station_id": source_station_id,
                "destination_id": destination_station_id,
            }
        )
    return formatted_connections
