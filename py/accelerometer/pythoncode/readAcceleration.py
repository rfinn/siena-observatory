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
import argparse

parser = argparse.ArgumentParser(description = 'This code reads acceleration from arduino over wireless upd connection.  An example of running the code from the command line is:   python plotAcceleration.py > junk-2017Mar25 --readNevents N')
parser.add_argument('--readNevents', dest = 'N', default=0,help = 'Number of data events to read.  If not set, the program will read until it is killed')


args = parser.parse_args()

UDP_IP = '10.26.1.65'
UDP_PORT = 23
BUFFER_SIZE = 1024 # not sure what the units of this are

keep_reading = True
s= None
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


s.sendto('ready for data', (UDP_IP, UDP_PORT))

if s is None:
    print('could not open socket')
    sys.exit(1)
else:
    data,addr = s.recvfrom(BUFFER_SIZE)
    #startTime = datetime.now()
    i=0
    
    if float(args.N) < 0.1:
        while keep_reading:
            print datetime.now().time(), s.recv(BUFFER_SIZE)
    else:
        while i < int(args.N):
            print datetime.now().time(), s.recv(BUFFER_SIZE)
            i += 1

    #endTime = datetime.now()
#print 'delta T =',endTime-startTime
