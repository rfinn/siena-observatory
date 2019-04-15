import smbus
from MMA8451_lib import *
import time
DEVICE_ADDRESS = 0x1d
MMA8451_REG_WHOAMI = 0x0D
bus = smbus.SMBus(1)

# enable 4G range
#fd.write8(MMA8451_REG_XYZ_DATA_CFG, MMA8451_RANGE_2_G.value)

def read8(DEVICE_ADDRESS,REG):
    x = bus.read_byte_data(DEVICE_ADDRESS,REG)
    if x > 127:
        x -= 256
    return x
def joinbits(msb,lsb):
    x = msb
    x <<= 8
    x |= lsb
    x >>= 2
    return x

def readvalue(DEVICE_ADDRESS,REG_MSB,REG_LSB):
    xmsb = read8(DEVICE_ADDRESS, REG_MSB)
    xlsb = read8(DEVICE_ADDRESS, REG_LSB)
    x=joinbits(xmsb,xlsb)
    return x

ret = bus.read_byte_data(DEVICE_ADDRESS, MMA8451_REG_WHOAMI)
print ret

for i in range(100):
    ax = readvalue(DEVICE_ADDRESS, MMA8451_REG_OUT_X_MSB,MMA8451_REG_OUT_X_LSB)
    ay = readvalue(DEVICE_ADDRESS, MMA8451_REG_OUT_Y_MSB,MMA8451_REG_OUT_Y_LSB)
    az = readvalue(DEVICE_ADDRESS, MMA8451_REG_OUT_Z_MSB,MMA8451_REG_OUT_Z_LSB)
    time.sleep(.1)
    print ax,ay,az

xmsb = read8(DEVICE_ADDRESS, MMA8451_REG_OUT_X_MSB)
xlsb = read8(DEVICE_ADDRESS, MMA8451_REG_OUT_X_LSB)
x = joinbits(xmsb,xlsb)


ymsb = bus.read_byte_data(DEVICE_ADDRESS, MMA8451_REG_OUT_Y_MSB)
if ymsb > 127 :
	ymsb -= 256
ylsb = bus.read_byte_data(DEVICE_ADDRESS, MMA8451_REG_OUT_Y_LSB)
if ylsb > 127 :
	ylsb -= 256
print xmsb,xlsb
x = ymsb
x <<= 8
x |= ylsb
x >>= 2
print x
zmsb = bus.read_byte_data(DEVICE_ADDRESS, MMA8451_REG_OUT_Z_MSB)
if zmsb > 127 :
	zmsb -= 256
zlsb = bus.read_byte_data(DEVICE_ADDRESS, MMA8451_REG_OUT_Z_LSB)
if zlsb > 127 :
	zlsb -= 256
print xmsb,xlsb
x = zmsb
x <<= 8
x |= zlsb
x >>= 2
print x

