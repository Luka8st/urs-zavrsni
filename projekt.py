import serial
import binascii
import time
from datetime import datetime, timedelta

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)
ser.close()
ser.open()

time1 = 0
time2 = 0

while True:
    data = str(binascii.hexlify(ser.read(17)))
    if data[6:22] != '':
        if time1 == 0:
            time1 = datetime.now()
            print("tag: '{}'".format(data[6:22]))
            print("time1: ", time1)
        else:
            time2 = datetime.now()
            print("tag: '{}'".format(data[6:22]))
            print("time2: ", time2)
            print("time between: ", time2 - time1)
            time1 = 0
    else:
        print("No tag detected...")
    time.sleep(1)
