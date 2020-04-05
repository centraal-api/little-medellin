

def get_day_hour(time_event: str):
    d,h = time_event.split('_')
    d = int(d.split('d')[1])
    h = int(h.split('h')[1])
    return d, h
    