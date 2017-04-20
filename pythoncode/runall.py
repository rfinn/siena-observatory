#! /usr/bin/env python 

import os
import glob

files = glob.glob('2017*.log')
#csvfiles = glob.glob('2017*-time.csv') # these exist after the plotting program has run


for f in files:
    froot,t = f.split('.')
    #print froot 
    if os.path.exists('plots/'+froot+'-avst.png'):
        print 'already ran for ',froot
        continue
    else:
        print 'running ',froot
        os.system('python ~/github/siena-observatory/pythoncode/plotAccelRpi.py --datfile '+froot+' --plot') 


#python ~/github/siena-observatory/pythoncode/plotAccelRpi.py --datfile 2017-04-14_00:00:13 --plot 
#python ~/github/siena-observatory/pythoncode/plotAccelRpi.py --datfile 2017-04-14_04:00:13 --plot 
#python ~/github/siena-observatory/pythoncode/plotAccelRpi.py --datfile 2017-04-14_08:00:13 --plot 
#python ~/github/siena-observatory/pythoncode/plotAccelRpi.py --datfile 2017-04-14_12:00:13 --plot 
#python ~/github/siena-observatory/pythoncode/plotAccelRpi.py --datfile 2017-04-14_16:00:15 --plot 

