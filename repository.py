import psycopg2
from psycopg2.extras import RealDictCursor

def connect():
    pg_config = {
        'host': 'pythonweekend.cikhbyfn2gm8.eu-west-1.rds.amazonaws.com',
        'database': 'pythonweekend',
        'user': 'shareduser',
        'password': 'NeverEverSharePasswordsInProductionEnvironement'
    }
    return psycopg2.connect(**pg_config)

def get_combinations(source, destination, date_from):
    sql = """
    SELECT t1.source, t1.destination, t1.departure_datetime,t1.arrival_datetime,
    t2.source as next_source, t2.destination as next_destination, 
    t2.departure_datetime as next_departure_datetime, t2.arrival_datetime as next_arrival_datetime
    from journeys_miso as t1
    inner join journeys_miso as t2
    on t1.destination = t2.source
    where t1.arrival_datetime < t2.departure_datetime
    and t1.source = %(source)s and t2.destination = %(destination)s
    and t1.departure_datetime > %(date_from)s
    """

    bindings = {
        'source': source,
        'destination': destination,
        'date_from': date_from
    }

    conn = connect()

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql, bindings)
        connections = cursor.fetchall()

    return connections

def insert_journey(
    source, destination, departure_datetime, arrival_datetime, carrier, vehicle_type, price, currency
):
    sql_insert = """
    INSERT INTO journeys_miso (source, destination, departure_datetime, arrival_datetime, carrier,
                          vehicle_type, price, currency)
    VALUES (%(source)s,
            %(destination)s,
        %(departure_datetime)s,
            %(arrival_datetime)s,
            %(carrier)s,
            %(vehicle_type)s,
            %(price)s,
            %(currency)s);
    """
    
    values = {
        "source": source, 
        "destination": destination, 
        "departure_datetime": departure_datetime, 
        "arrival_datetime": arrival_datetime,
        "carrier": carrier,
        "vehicle_type": vehicle_type,
        "price": price,
        "currency": currency
    }

    conn = connect()
    
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(sql_insert, values)
        conn.commit()
