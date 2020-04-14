
from datetime import datetime

def get_day_hour(time_event: str):
    d,h = time_event.split('_')
    d = int(d.split('d')[1])
    h = int(h.split('h')[1])
    return d, h

def get_timestamp(time_event: str):
    initial_day = datetime.timestamp(datetime(2019,1,1))
    d,h=get_day_hour(time_event)
    timestamp = initial_day + 3600*24*d + (3600.0*24)/5*h
    return(timestamp)
    