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

FX29_loadrange = 100
FX29_zeroforce = 1000
FX29_fullforce = 15000

mass_now = 1

while True:
    
    with I2CDevice(tca[0], DEVICE_ADDRESS) as lc1:

        lc1.readinto(lc1_read)
        status1 = (lc1_read[0] & 0xC0) >> 6
        print("LC 1 status - {}".format(status1))
        measurement1 = ((lc1_read[0] & 0x3F) << 8) | (lc1_read[1] & 0xFF)
        loadlb_1 = ((measurement1-FX29_zeroforce)*FX29_loadrange)/(FX29_fullforce-FX29_zeroforce)
    
    with I2CDevice(tca[4], DEVICE_ADDRESS) as lc2:

        lc2.readinto(lc2_read)
        status2 = (lc2_read[0] & 0xC0) >> 6
        print("LC 2 status - {}".format(status2))
        measurement2 = ((lc2_read[0] & 0x3F) << 8) | (lc2_read[1] & 0xFF)
        loadlb_2 = ((measurement2-FX29_zeroforce)*FX29_loadrange)/(FX29_fullforce-FX29_zeroforce)
    
    bed_mass = loadlb_1 + loadlb_2

    if abs(bed_mass - mass_now) > .2:
        print("{} lbs detected".format(bed_mass))
        mass_now = bed_mass

    time.sleep(1)
    
