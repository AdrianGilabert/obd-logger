#!/bin/bash
echo $DISPLAY
export DISPLAY=:0
/usr/bin/python3 /home/pi/obd-logger/main.py &
exit
