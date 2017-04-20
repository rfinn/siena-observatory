
'''
from
https:#github.com/iseeag/MMA8451/blob/master/wiringPi_MMA8451.cpp


#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <wiringPiI2C.h>
#include <unistd.h>
#include "wiringPi_MMA8451.h"

'''

import sys
sys.path.append('~/github/siena-observatory/pythonCode/')

from MMA8451_lib import *
import time
import I2C


# get updated g from sensors using joinbits(reg, reg)


def setup(devId) :
    #fd = get_i2c_device(devId)

    return fd
class myDevice(I2C.Device):
    '''
    # basic i2c read/write
    def readS8(self,reg):
        return self.ReadReg8(fd,reg)


    def write8(self,reg, sig) :
        self.WriteReg8(fd,reg,sig)

        # join bits of XYZ_MSB and XYZ_LSB, using readS8(reg)/getRange(void)
    # should make a function setRange(self)
    '''


    def joinbits(self, msb_reg, lsb_reg) :
        #int16_t xyz
        
        xyz = self.readS8(msb_reg)  ###??? read signed or unsigned bit? - I think signed
        xyz <<= 8
        xyz = xyz | self.readS8(lsb_reg)
        xyz >>= 2
        return float(xyz/self.divider)

    

    
    def getRange(self):  # find out the range as the last three bits of MMA8451_REG_XYZ_DATA_CFG
        r8=self.readS8(MMA8451_REG_XYZ_DATA_CFG)
        print 'r8 = ',r8
        self.range=mma8451_range_t(r8 & 0x03)

        if(self.range.name == MMA8451_RANGE_8_G): self.divider = 1024
        elif(self.range.name == MMA8451_RANGE_4_G): self.divider = 2048
        elif(self.range.name == MMA8451_RANGE_2_G): self.divider = 4096 
        else:
            print 'problem with range!!!!'
            sys.exit()
    def update_3_g(self) :
        x = self.joinbits(MMA8451_REG_OUT_X_MSB,MMA8451_REG_OUT_X_LSB)
        y = self.joinbits(MMA8451_REG_OUT_Y_MSB,MMA8451_REG_OUT_Y_LSB)
        z = self.joinbits(MMA8451_REG_OUT_Z_MSB,MMA8451_REG_OUT_Z_LSB)
        return x,y,z




if __name__ == "__main__":

    BUSNUM = I2C.get_default_bus()
    print 'BUSNUM = ',BUSNUM
    print '1'
    fd = myDevice(MMA8451_DEFAULT_ADDRESS,BUSNUM)
    print '1a'
    fd.write8(MMA8451_REG_XYZ_DATA_CFG, 0b01)
    print '1b'
    r8=fd.readS8(MMA8451_REG_XYZ_DATA_CFG)
    print 'r8 = ',r8
    fd.write8(MMA8451_REG_CTRL_REG2, 0x40)
    print '1c'
    fd.getRange()
    # reset
    print '2'
    fd.write8(MMA8451_REG_CTRL_REG2, 0x40) 
    time.sleep(.5)
    print '3'

    time.sleep(.5)
    print '4'
    # High res
    fd.write8(MMA8451_REG_CTRL_REG2, 0x12)
    time.sleep(.5)
    print '5'
    # Low noise @100Hz output rate, where 800Hz is the max
    fd.write8(MMA8451_REG_CTRL_REG1, (MMA8451_DATARATE_100_HZ | MMA8451_L_NS))
    time.sleep(.50)
    print '6'
    # Activate! 
    fd.write8(MMA8451_REG_CTRL_REG1, (fd.readS8(MMA8451_REG_CTRL_REG1) | 0x01))
    time.sleep(.5)
    print '7'
    deviceid = fd.readS8(MMA8451_REG_WHOAMI)
    if(deviceid != MMA8451_DEVICE_ID) :
        flag=false
    else:
        print("MMA8451 activated! \n")
    

    # update the gs
    while(true):
        x_g,y_g,z_g = fd.update_3_g()
        printf("g of x: %6.4f y: %6.4f z: %6.4f\n"%( x_g, y_g, z_g))
        time.sleep(.5)
    

    


## # debugging function
## const char *byte_to_binary(int x) :
##     static char b[9]
##     b[0] = '\0'
##     int z
##     for (z = 128 z > 0 z >>= 1) :
##         strcat(b, ((x & z) == z) ? "1" : "0")
    
##     return b


## # debugging function 
## void foread() :
##     for(uint8_t i=0x00 i < 0x2E i++) :
##         reg8=readS8(i)
##         printf "%04x list: %6hd 0x%.2X %s\n"%( i, reg8,reg8,byte_to_binary(reg8))
    

