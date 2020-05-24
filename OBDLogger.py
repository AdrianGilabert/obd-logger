import curses
import logging
import time
import obd
import utils
import geocoder
from influxdb import InfluxDBClient
from obd import OBDStatus
from setup import OBD_SECUENCES, OBD_LOCATION, DATABASE_CONFIG, CAR_NAME


class OBDLogger:
    def __init__(self, stdscr):
        self.client = InfluxDBClient(DATABASE_CONFIG['url'],
                                     DATABASE_CONFIG['port'],
                                     DATABASE_CONFIG['user'],
                                     DATABASE_CONFIG['password'],
                                     DATABASE_CONFIG['database_name'])
        self.screen = stdscr
        self.database_status = OBDStatus.NOT_CONNECTED
        self.obd_status = OBDStatus.NOT_CONNECTED
        self.gps_status = OBDStatus.NOT_CONNECTED
        self.errors = 0
        logging.getLogger('obd').setLevel(logging.FATAL)
        curses.curs_set(0)
        self.status_refresh()

    def main(self):

        self.check_obd_status()
        connection = obd.OBD(OBD_LOCATION)

        self.check_database_status()

        started_at = int(round(time.time() * 1000))


        json_body = []

        count = 0

        while True:

            for commands in OBD_SECUENCES:
                if count % commands['interval'] == 0:
                    for command in commands['commands']:
                        response = connection.query(command['command'], force=True)
                        json_body.append(utils.json_build(command['name'],
                                                          CAR_NAME, started_at, response.value.magnitude))
                    latitude, longitude = self.get_gps()
                    json_body.append(utils.json_gps_build(CAR_NAME, started_at, latitude, longitude))

                time.sleep(OBD_SECUENCES[0]['interval'])

            count = count + OBD_SECUENCES[0]['interval']

            try:
                data = self.client.write_points(json_body)
                json_body = []
                self.errors = 0
                self.database_status = 'Connected'

            except:
                self.errors = self.errors + 1
                self.database_status = 'Reconnecting'

            finally:
                self.status_refresh()

    def check_obd_status(self):
        while self.obd_status == OBDStatus.NOT_CONNECTED:
            try:
                connection = obd.OBD(OBD_LOCATION)
                self.obd_status = connection.status()
            except:
                self.obd_status = OBDStatus.NOT_CONNECTED
                time.sleep(10)
        self.status_refresh()

    def check_database_status(self):
        while self.database_status == OBDStatus.NOT_CONNECTED:
            try:
                self.client.ping()
                self.database_status = 'Connected'

            except:
                self.database_status = OBDStatus.NOT_CONNECTED

            time.sleep(10)
        self.status_refresh()

    def get_gps(self):
        g = geocoder.ip('me')
        return g.latlng

    def status_refresh(self):
        self.screen.clear()
        self.screen.addstr(2, 2, 'Status OBD: ')
        self.screen.addstr(2, 20, self.obd_status)
        self.screen.addstr(4, 2, 'Status InfluxDB: ')
        self.screen.addstr(4, 20, self.database_status)
        self.screen.addstr(6, 2, 'Status GPS: ')
        self.screen.addstr(6, 20, self.gps_status)
        self.screen.addstr(8, 2, 'Errors: ')
        self.screen.addstr(8, 20, str(self.errors))
        self.screen.refresh()
