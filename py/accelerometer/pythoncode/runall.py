#! /usr/bin/env python 

import os
import glob
import argparse

parser = argparse.ArgumentParser(description = 'This code runs plotAccelRpi.py for all files that match the input string and that do not already have an associated fft figure in the plots subdirectory.')
parser.add_argument('--string', dest = 'string', default='2017',help = 'filename string ')
args = parser.parse_args()

s = args.string+'*.log'
print s
files = glob.glob(args.string+'*.log')
#print files
#csvfiles = glob.glob('2017*-time.csv') # these exist after the plotting program has run


for f in files:
    froot,t = f.split('.')
    #print froot 
    #if os.path.exists('plots/'+froot+'-avst.png'):
    if os.path.exists('plots/'+froot+'-fft.png'):
        print 'already ran for ',froot
        continue
    else:
        print 'running ',froot
        #os.system('python ~/github/siena-observatory/pythoncode/plotAccelRpi.py --datfile '+froot+' --plot')
        os.system('python ~/github/siena-observatory/pythoncode/plotAccelRpi.py --datfile '+froot+' --plot --fourier') 


#python ~/github/siena-observatory/pythoncode/plotAccelRpi.py --datfile 2017-04-14_00:00:13 --plot 
#python ~/github/siena-observatory/pythoncode/plotAccelRpi.py --datfile 2017-04-14_04:00:13 --plot 
#python ~/github/siena-observatory/pythoncode/plotAccelRpi.py --datfile 2017-04-14_08:00:13 --plot 
#python ~/github/siena-observatory/pythoncode/plotAccelRpi.py --datfile 2017-04-14_12:00:13 --plot 
#python ~/github/siena-observatory/pythoncode/plotAccelRpi.py --datfile 2017-04-14_16:00:15 --plot 

