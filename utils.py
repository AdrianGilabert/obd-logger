import time


def json_build(name, car, started_at, value):
    return {
        'measurement': name,
        'tags': {
            'car': car,
            'started_at': started_at
        },
        'time': int(time.time() * 1000000000)
        ,
        'fields': {
            'value': value
        }
    }


def json_gps_build(car, started_at, latitude=0, longitude=0):
    return {
        'measurement': 'gps',
        'tags': {
            'car': car,
            'started_at': started_at,
            'latitude': latitude,
            'longitude': longitude
        },
        'time': int(time.time() * 1000000000)
        ,
        'fields': {
            'value': 0
        }
    }
