#!/usr/bin/env python

'''
GOAL:
   To connect to arduino wifi101 card and receive data from accelerometer.

USAGE:
   To run from the command line:

   python readAcceleration.py > junk-2017Mar25

PROCEDURE:
   Right now, this is set to receive 1000 data points.
   We can remove the counter once we are ready for real data collection.

WRITTEN BY:
   Rose A. Finn
   2017-Mar-26
   
'''

import socket
from datetime import datetime
from datetime import timedelta

UDP_IP = '10.26.1.65'
UDP_PORT = 23
BUFFER_SIZE = 4 # not sure what the units of this are

s= None
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.sendto('hello', (UDP_IP, UDP_PORT))

if s is None:
    print('could not open socket')
    sys.exit(1)
else:
    data,addr = s.recvfrom(BUFFER_SIZE)
    #startTime = datetime.now()
    i=0
    while i < 4004:
        print datetime.now().time(), s.recv(BUFFER_SIZE)
        i += 1
    #endTime = datetime.now()
#print 'delta T =',endTime-startTime
