import time
import utils
import obd
from influxdb import InfluxDBClient

from setup import OBD_SECUENCES, OBD_LOCATION, DATABASE_CONFIG, CAR_NAME

connection = obd.OBD(OBD_LOCATION)

client = InfluxDBClient(DATABASE_CONFIG['url'],
                        DATABASE_CONFIG['port'],
                        DATABASE_CONFIG['user'],
                        DATABASE_CONFIG['password'],
                        DATABASE_CONFIG['database_name'])

started_at = int(round(time.time() * 1000))

latitude = 0
longitude = 0

json_body = []

count = 0

while True:

    for commands in OBD_SECUENCES:
        if count % commands['interval'] == 0:
            for command in commands['commands']:
                response = connection.query(command['command'], force=True)
                json_body.append(utils.json_build(command['name'],
                                                  CAR_NAME, started_at, response.value.magnitude))
            latitude = latitude + 0.0001
            longitude = longitude + 0.0001

            json_body.append(utils.json_gps_build(CAR_NAME, started_at, latitude, longitude))

        time.sleep(OBD_SECUENCES[0]['interval'])

    count = count + OBD_SECUENCES[0]['interval']

    try:
        data = client.write_points(json_body)
        json_body = []
    except:
        print(json_body)
