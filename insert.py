import argparse
from connections import get_connections
from format import format_connections
from pprint import pprint
from repository import insert_journey

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str, nargs="+")
    parser.add_argument("--destination", type=str, nargs="+")
    parser.add_argument("--departure_date", type=str, nargs="+")
    args = parser.parse_args()

    return {
        "source": args.source[0],
        "destination": args.destination[0],
        "departure_date": args.departure_date[0],
    }


if __name__ == "__main__":
    arguments = get_arguments()
    connections = get_connections(
        arguments["source"], arguments["destination"], arguments["departure_date"]
    )
    connections = format_connections(connections)
    for connection in connections:
        for vehicle_type in connection['type']:
            insert_journey(
                source=connection['source_city'],
                destination=connection['destination_city'],
                departure_datetime=connection['departure_datetime'],
                arrival_datetime=connection['arrival_datetime'],
                carrier=connection['carrier'],
                vehicle_type=vehicle_type,
                price=connection['price'],
                currency="eur"
            )
