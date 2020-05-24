# obd-logger

1 Configurar pc de servidor:

En este PC se subiran los archivos desde la raspberry que hay en el coche por tanto debe estar encendido 24/7, ya que la potencia necesaria para la aplicacion es bastante baja se puede usar otra raspberry pero ha de ser con linux y docker instalado



1.1- Instalar InfluxDB:


docker run -p 8086:8086 \
      -v influxdb:/var/lib/influxdb \
      influxdb
      
crear base de datos

docker exec -it CONTAINER_ID /bin/bash

influxdb

create database obd
      
      
1.2- Instalar grafana:

docker run -d \
-p 3000:3000 \
--name=grafana \
-e "GF_INSTALL_PLUGINS=grafana-worldmap-panel" \
grafana/grafana:6.7.3

configurar data source

acceder a http:ip_server:3000 con usuario admin y contraseña admin

acceder a la rueda de configuracion, añadir data source, seleccionar influxdb y introducir los siguientes campos.

url:http://ip_server:8086 por ejemplo http://192.168.2.61:8086

database:obd
usuario:root
contraseña:root

y guardar

ahora clickar en el simbolo mas y importar un dashboard, aqui pegamos el contenido que hay en el fichero dynamic_dashboard.json

ahora el pc del servidor ya estaria listo pero debeis de tener en cuenta que para que la raspberry del coche pueda acceder el pc servidor debera ser accesible ya sea abriendo puertos, con vpn, zerotier o si es para pruebas se podria instalar todo en la misma raspberry.


2-Configurar raspberry
 
 
 2.1 Instalar raspbian
 
  
 
 2.2 instalar git:
 
 sudo apt-get install git
 
2.3 Descargar y configurar proyecto
 
 git clone https://github.com/AdrianGilabert/obd-logger.git
 
 abrir setup.py y cambiar las siguientes variables
 
 OBD_LOCATION = '/dev/pts/1'

esta es la ubicacion del obd, aqui la documentacion para configurarlo por bluetooth, yo para las pruebas he usado el siguiente emulador 
https://github.com/Ircama/ELM327-emulator

https://python-obd.readthedocs.io/en/latest/

DATABASE_CONFIG = {'url': '192.168.2.61',
                   'port': 8086,
                   'user': 'root',
                   'password': 'root',
                   'database_name': 'obd'
                   
aqui se configura la base datos donde se guardan los archivos, en este caso habria que cambiar la url con la ip de tu server.


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

por ultimo esto es lo que se desea registrar desde el obd, el interval son los segundos, por ejemplo si deseo que guarde la temperatura del refrigerante se pondria un 2 y deseo que se actualice cada medio segundo seria un 0.5 , el name es nombre que se le desea poner a ese registro, este va a gustos se puede poner cualquiera, en command es el comando del obd por ejemplo si deseo obtener el novel de gasolina el coamndo seria este.
 obd.commands.FUEL_LEVEL.
 
 por ejemplo si deseo añadir el registro del nivel de gasolina cada 30 segundos la configuracion quedaria asi
 
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
     {
        'interval': 30,
        'commands': [
            {'name': 'fuel_level', 'command': obd.commands.FUEL_LEVEL},
        ]
    }
]


2.4 Ejecutar proyecto:

cd obd-logger

pip3 install -r requeriments.txt

python3 main.py