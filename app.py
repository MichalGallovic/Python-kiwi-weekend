from flask import Flask, request, jsonify, render_template
from connections import get_connections, connection_hash
from locations import load_cities
from format import format_connections
from date_range import date_range
from redis_util import get_redis
from datetime import datetime, timedelta
from forms import SearchForm
from slugify import slugify

app = Flask(__name__)
app.config["PROPAGATE_EXCEPTIONS"] = True

def format_datetime(value, format='%m.%d %H:%M'):
    return datetime.strptime(value, '%Y-%m-%d %H:%M:%S').strftime(format)

app.jinja_env.filters['datetime'] = format_datetime

def filter_by_date(connections, date_to):
    return [c for c in connections if (datetime.strptime(c["arrival_datetime"], '%Y-%m-%d %H:%M:%S') <= datetime.strptime(date_to, '%Y-%m-%d') + timedelta(days=1))]

def filter_by_passengers(connections, passengers):
    return [c for c in connections if c["free_seats"] > int(passengers)]

def find_connections(source, destination, date_from, date_to, passengers=None):
    if not date_to:
        date_to = date_from

    dates = date_range(date_from, date_to)
    connections_for_date = []

    for date in dates:
        connections_for_date.append(
            format_connections(get_connections(source, destination, date))
        )

    connections = {
        connection_hash(connection): connection
        for connections in connections_for_date
        for connection in connections
    }

    connections = [connection for hash, connection in connections.items()]
    connections = [connection for connection in connections if connection['free_seats'] > 0]
    connections = filter_by_date(connections, date_to)
    
    if passengers:
        connections = filter_by_passengers(connections, passengers)

    return connections

@app.route("/api/search")
def search():
    source = request.args.get("source")
    destination = request.args.get("destination")
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    passengers = request.args.get("passengers")

    connections = find_connections(source, destination, date_from, date_to, passengers)
    return jsonify(connections)

@app.route('/api/locations-search')
def autocomplete():
    term = slugify(request.args.get('term', '').lower())
    cities = load_cities()
    return jsonify([x["name"] for x in cities if term in slugify(x['name']).lower()])

@app.route("/search", methods=["GET", "POST"])
def index():
    form = SearchForm(csrf_enabled=False)

    connections = []

    if form.validate_on_submit():
        source = request.form.get("source")
        destination = request.form.get("destination")
        date_from = request.form.get("departure_date")
        date_to = request.form.get("arrival_date")
        connections = find_connections(source, destination, date_from, date_to)

    return render_template('index.html', connections=connections, form=form)

if __name__ == "__main__":
    app.run(debug=True)
