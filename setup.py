import obd
OBD_LOCATION = '/dev/pts/1'

DATABASE_CONFIG = {'url': '192.168.2.61',
                   'port': 8086,
                   'user': 'root',
                   'password': 'root',
                   'database_name': 'obd'
                   }
CAR_NAME = 'cruze'

OBD_SECUENCES = [

    {
        'interval': 1,
        'commands': [
            {'name': 'speed', 'command': obd.commands.SPEED},
            {'name': 'rpm', 'command': obd.commands.RPM},
        ]
    },

    {
        'interval': 2,
        'commands': [
            {'name': 'coolant_temperature', 'command': obd.commands.COOLANT_TEMP},
        ]
    }
]
