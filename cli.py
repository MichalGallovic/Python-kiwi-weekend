import argparse
from connections import get_connections
from format import format_connections
from pprint import pprint


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

    pprint(format_connections(connections))
