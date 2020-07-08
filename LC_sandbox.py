import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice
import time

DEVICE_ADDRESS = 0x28
i2c_port = busio.I2C(board.SCL, board.SDA)

command = DEVICE_ADDRESS << 1 | 1
s_command = (command).to_bytes(1, byteorder = 'big')
result = bytearray(2)

device = I2CDevice(i2c_port, DEVICE_ADDRESS)

FX29_loadrange = 100
FX29_zeroforce = 1000
FX29_fullforce = 15000

with device:
    store = 1
    
    while True:
        
        device.write(s_command, start = 0, stop = True)
        device.readinto(result)

        status = (result[0] & 0xC0) >>6
        check = (result[0]<<8)
        measurement = ((result[0] & 0x3F) << 8) | (result[1] & 0xFF)
        forcelb = ((measurement-FX29_zeroforce)*FX29_loadrange)/(FX29_fullforce-FX29_zeroforce)
        
        if abs(forcelb - store) > .2:
            print("{} pounds of FORCE".format(forcelb))
            #print(measurement)
            #print(status)
            #print(check)
            store = forcelb
        
        time.sleep(2)
