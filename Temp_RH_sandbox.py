#temp&RH
import time
from micropython import const
import board
import busio
import adafruit_si7021
import csv

i2c_port = busio.I2C(board.SCL, board.SDA)
_USER1_VAL = const(0x3A)
sensor = adafruit_si7021.SI7021(i2c_port)

print('Temperature: {} degrees C'.format(sensor.temperature))
print('Humidity: {}%'.format(sensor.relative_humidity))


temp = []
humid = []
endtime = time.time() + 21


while True:
    temp.append(sensor.temperature)
    humid.append(sensor.relative_humidity)
    if time.time() > endtime:
        break
    time.sleep(2)
    
with open('temprh.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(temp)
    writer.writerow(humid)

print("Done, new file")