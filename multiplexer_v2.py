import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_tca9548a
import time

DEVICE_ADDRESS = 0x28
i2c_port = busio.I2C(board.SCL, board.SDA)
i2c_port.scan()
tca = adafruit_tca9548a.TCA9548A(i2c_port)

lc1_read = bytearray(2)
lc2_read = bytearray(2)

command = DEVICE_ADDRESS << 1 | 1
s_command = (command).to_bytes(1, byteorder = 'big')

lc1 = I2CDevice(tca[4], DEVICE_ADDRESS)
lc2 = I2CDevice(tca[2], DEVICE_ADDRESS)

FX29_loadrange = 100
FX29_zeroforce = 1000
FX29_fullforce = 15000

mass_now = 1
    
while True:
    with lc1:        
        #lc1.write(s_command, start = 0, stop = True)
        lc1.readinto(lc1_read)
        time.sleep(.2)
        status1 = (lc1_read[0] & 0xC0) >> 6
        #print("LC 1 status - {}".format(status1))
        measurement1 = ((lc1_read[0] & 0x3F) << 8) | (lc1_read[1] & 0xFF)
        loadlb_1 = ((measurement1-FX29_zeroforce)*FX29_loadrange)/(FX29_fullforce-FX29_zeroforce)
        #print(measurement1)
        
    with lc2:       
        #lc2.write(s_command, start = 0, stop = True)
        lc2.readinto(lc2_read)
        time.sleep(.2)
        status2 = (lc2_read[0] & 0xC0) >> 6
        #print("LC 2 status - {}".format(status2))
        measurement2 = ((lc2_read[0] & 0x3F) << 8) | (lc2_read[1] & 0xFF)
        loadlb_2 = ((measurement2-FX29_zeroforce)*FX29_loadrange)/(FX29_fullforce-FX29_zeroforce)
        #print(measurement2)

    bed_mass = loadlb_1 + loadlb_2

    if abs(bed_mass - mass_now) > .2:
        print("{} lbs detected".format(bed_mass))
        mass_now = bed_mass

    time.sleep(1)

