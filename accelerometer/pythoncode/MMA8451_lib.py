#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <wiringPiI2C.h>
#include <unistd.h>
#include <stdbool.h>

#ifndef _MMA8451_H_

#define _MMA8451_H_

##include "I2Cdev.h"f
from enum import Enum

MMA8451_ADDRESS_AD0_LOW =    0x1C # address pin low (GND), default for InvenSense evaluation board
MMA8451_ADDRESS_AD0_HIGH=    0x1D # address pin high (VCC)
MMA8451_DEFAULT_ADDRESS =    MMA8451_ADDRESS_AD0_LOW
MMA8451_DEVICE_ID       =    0x1A # of REG_WHOAMI

MMA8451_REG_OUT_X_MSB   =  0x01
MMA8451_REG_OUT_X_LSB   =  0x02
MMA8451_REG_OUT_Y_MSB   =  0x03
MMA8451_REG_OUT_Y_LSB   =  0x04
MMA8451_REG_OUT_Z_MSB   =  0x05
MMA8451_REG_OUT_Z_LSB   =  0x06
MMA8451_REG_SYSMOD      =  0x0B
MMA8451_REG_WHOAMI      =  0x0D
MMA8451_REG_XYZ_DATA_CFG=  0x0E
MMA8451_REG_PL_STATUS   =  0x10
MMA8451_REG_PL_CFG      =  0x11
MMA8451_REG_CTRL_REG1   =  0x2A
MMA8451_REG_CTRL_REG2   =  0x2B # reset: 01000000 High Resolution: 00010010
MMA8451_REG_CTRL_REG4   =  0x2D
MMA8451_REG_CTRL_REG5   =  0x2E


MMA8451_PL_PUF          =  0
MMA8451_PL_PUB          =  1
MMA8451_PL_PDF          =  2
MMA8451_PL_PDB          =  3
MMA8451_PL_LRF          =  4  
MMA8451_PL_LRB          =  5  
MMA8451_PL_LLF          =  6  
MMA8451_PL_LLB          =  7  

MMA8451_L_NS             = 0x04


#### need john's help to continue


class mma8451_range_t(Enum):
  MMA8451_RANGE_8_G           = 0b10   # +/- 8g
  MMA8451_RANGE_4_G           = 0b01   # +/- 4g
  MMA8451_RANGE_2_G           = 0b00    # +/- 2g (default value)


#/* Used with register 0x2A (MMA8451_REG_CTRL_REG1) to set bandwidth */
class mma8451_dataRate_t(Enum):

  MMA8451_DATARATE_800_HZ     = 0b000 #  400Hz 
  MMA8451_DATARATE_400_HZ     = 0b001 #  200Hz
  MMA8451_DATARATE_200_HZ     = 0b010 #  100Hz
  MMA8451_DATARATE_100_HZ     = 0b011 #   50Hz
  MMA8451_DATARATE_50_HZ      = 0b100 #   25Hz
  MMA8451_DATARATE_12_5_HZ    = 0b101 # 6.25Hz
  MMA8451_DATARATE_6_25HZ     = 0b110 # 3.13Hz
  MMA8451_DATARATE_1_56_HZ    = 0b111 # 1.56Hz


'''
I think these are definitions I don't need

uint8_t read8(uint8_t reg);
void write8(uint8_t reg, uint8_t sig);
mma8451_range_t getRange(void);
bool setup(int32_t devId);
float join(uint8_t msb_reg, uint8_t lsb_reg);
void update_3_g(float *x, float *y, float *z);

#debugging 
const char *byte_to_binary(int x);
void foread(void);


#endif /* _MMA8451_H_ */

'''
