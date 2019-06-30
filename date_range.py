import datetime

def date_range(date_from, date_to):
    dates = []
    date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d')
    date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d')
    date_delta = date_to - date_from
    
    for i in range(0, date_delta.days + 1):
        new_date = date_from + datetime.timedelta(days=i)
        dates.append(new_date.strftime('%Y-%m-%d'))

    return dates