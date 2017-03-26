#! /usr/bin/env python
'''
GOAL:
   To read in output from readAcceleration.py.
   This code will generate:
   - csv file of the data, with format
      - xtime, ax, ytime, ay, ztime, az
   - plots of acceleration vs time and power vs frequency

   The plots can be made using matplotlib (set --plot flag)
   or plotly (set --plotly flag).

USEAGE:
   An example of running the code from the command line is

   python plotAcceleration.py --datfile junk-2017Mar25

   To run and generate figures using matplotlib

   python plotAcceleration.py --datfile junk-2017Mar25 --plot

   

PROCEFURE:
   This code uses the Lomb Scargle method to calculate the FFT for data
   that are taken at unequal time intervals.  See

   http://docs.astropy.org/en/stable/stats/lombscargle.html

WRITTEN BY:
   Rose A. Finn
   2017-Mar-26
   
'''

import numpy as np
import argparse
import dateutil.parser
import datetime as dt
from astropy.stats import LombScargle



parser = argparse.ArgumentParser(description = 'This code creates a csv file and plots data from accelerometer.  Data file is generated from readAcceleration.py.  An example of running the code from the command line is:   python plotData.py --datfile junk-2017Mar25 --plot')
parser.add_argument('--datfile', dest = 'datfile', default='fake_data',help = 'filename that contains data from accelerometer.  default is junk-2017Mar25')
parser.add_argument('--plot', dest = 'plot', default = False, action = 'store_true', help = 'generate plot of acceleration data and FFT using matplotlib.  Figure is saved as acceleration-vs-time.png.  default is False.')
parser.add_argument('--plotly', dest = 'plotly', default = False, action = 'store_true', help = 'generate plot of acceleration data on plotly.  default is False.  ')

args = parser.parse_args()
if args.plot:
    from matplotlib import pyplot as plt

if args.plotly:
    import plotly
    plotly.tools.set_credentials_file(username='rfinn',api_key='SloMwvUVB3WZigJggyEd')
    plotly.tools.set_config_file(world_readable=True,sharing='public')
    import plotly.plotly as py
    import plotly.graph_objs as go

## Read in data file
print args.datfile
infile1 = open(args.datfile,'r')
nlines=0
for line in infile1:
    if line.find('N') > -1:
        nlines += 1
infile1.close()
print 'number of data points = ',nlines

# set up data arrays
tx = np.zeros(nlines,dtype='datetime64[ms]') # time stamp
ty = np.zeros(nlines,dtype='datetime64[ms]') # time stamp
tz = np.zeros(nlines,dtype='datetime64[ms]') # time stamp
ax = np.zeros(nlines) # x acceleration
ay = np.zeros(nlines) # y acceleration
az = np.zeros(nlines) # z acceleration


# read in data file
infile1 = open(args.datfile,'r')
ncount=0
i = 0
for line in infile1:
    if line.find('Hello') > -1:
        continue
    if len(line) < 1: # skip blank lines
        continue
    if line.find('N') > -1:
        ncount = 1
        continue
    else:
        f = line.split()
        #print f
    if len(f) < 1:
        continue
    if ncount == 1:
        tx[i] = dateutil.parser.parse(str(f[0]))#, '%H:%M:%S:%f')
        ax[i] = float(f[1])
        ncount += 1
        #i += 1
        continue
    elif ncount == 2:
        ty[i] = dateutil.parser.parse(str(f[0]))
        ay[i] = float(f[1])
        ncount += 1
        #i += 1
        continue
    if ncount == 3:
        tz[i] = dateutil.parser.parse(str(f[0])) 
        az[i] = float(f[1])
        ncount = 0
        i += 1
        continue
infile1.close()

# convert acceleration to m/s^2
range=2. # range of accelerometer in +/- __ G
nbits = 14
g = 9.8 # acceleration of gravity in m/s^2
astep = (range*g/(2**(nbits-1)))
ax = ax*astep
ay = ay*astep
az = az*astep         


deltatx = np.array((tx - tx[0])/1000.,float)
deltaty = np.array((ty - ty[0])/1000.,float)
deltatz = np.array((tz - tz[0])/1000.,float)

freqx, powerx = LombScargle(deltatx,ax).autopower()
freqy, powery = LombScargle(deltaty,ay).autopower()
freqz, powerz = LombScargle(deltatz,az).autopower()

# write out data as csv?
alldat = np.zeros((nlines,6))
alldat[:,0] = deltatx
alldat[:,1] = ax
alldat[:,0] = deltaty
alldat[:,1] = ay
alldat[:,0] = deltatz
alldat[:,1] = az

#outfile = open(datfile+'.csv','w')
np.savetxt(args.datfile+'.csv',alldat,fmt='%.8e',delimiter=',')

if args.plot:
    plt.figure(figsize=(10,6))
    plt.subplots_adjust(hspace=.3,top=.95,left=.1,right=.95)
    plt.subplot(2,1,1)
    plt.scatter(tx,ax-np.mean(ax),s=10,c='c',edgecolors='None',label='ax')
    plt.scatter(ty,ay-np.mean(ay)+.2,s=10,c='orange',edgecolors='None',label='ay')
    plt.scatter(tz,az-np.mean(az)-.2,s=10,c='g',edgecolors='None',label='az')
    plt.xlabel('$Time$', fontsize=16)
    plt.ylabel('$Acceleration \ (m/s^2) $',fontsize=16)
    plt.legend(loc='upper right',scatterpoints=1)
    plt.xlim(min(tx),max(tx))
    plt.subplot(2,1,2)
    plt.scatter(freqx,np.abs(powerx),s=10,c='c',edgecolors='None',label='ax')
    plt.scatter(freqy,np.abs(powery),s=10,c='orange',edgecolors='None',label='ax')
    plt.scatter(freqz,np.abs(powerz),s=10,c='g',edgecolors='None',label='ax')
    plt.xlabel('$Frequency \ (Hz)$',fontsize=16)
    plt.ylabel('$Power$',fontsize=16)
    plt.xlim(0,250.)
    plt.savefig('acceleration-vs-time.png')
    
    
if args.plotly:


    trace0 = go.Scatter(x=tx,y=ax,
                    mode='markers',
                    name='ax',
                    )
    trace1 = go.Scatter(x=ty,y=ay,mode='markers',name='ay')
    trace2 = go.Scatter(x=tz,y=az,mode='markers',name='az')
    data = go.Data([trace0,trace1, trace2])

    layout = go.Layout(dict(title = 'Acceleration vs. Time',
              xaxis = dict(title = 'Time (HH:MM:SS)'),
              yaxis = dict(title = 'Acceleration  (m/s^2)')))

    '''
    fig = plotly.tools.make_subplots(rows=2, cols=1)
    fig.append_trace(trace0, 1, 1)
    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 1, 1)
    fig['layout'].update(title='Acceleration vs Time')
    '''
    fig = go.Figure(data = data, layout=layout)


    



    '''
    trace3 = go.Scatter(x=freqx,y=powerx,
                    mode='markers',
                    name='FFTx',
                    )
    trace4 = go.Scatter(x=freqy,y=powery,mode='markers',name='FFTy')
    trace5 = go.Scatter(x=freqz,y=powerz,mode='markers',name='FFTz')
    data2 = go.Data([trace3,trace4, trace5])
    fig.append_trace(trace3, 2, 1)
    fig.append_trace(trace4, 2, 1)
    fig.append_trace(trace5, 2, 1)    
    
    '''
    py.plot(fig, filename = 'acceleration-data')
