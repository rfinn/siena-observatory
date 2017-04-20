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

   

PROCEDURE:
   This code uses the Lomb Scargle method to calculate the FFT for data
   that are taken at unequal time intervals.  See

   http://docs.astropy.org/en/stable/stats/lombscargle.html

WRITTEN BY:
   Rose A. Finn
   2017-Mar-26

   updated 2017-Apr-09 to read file from data logger
   updated 2017-Apr-11 to read file from raspberry pi
   
'''

import numpy as np
import argparse
import dateutil.parser
import datetime as dt
from astropy.stats import LombScargle
import matplotlib.dates as mdates


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
nlines=len(infile1.readlines())
infile1.close()
print 'number of data points = ',nlines
nlines = nlines -1
# set up data arrays
t = np.zeros(nlines,dtype='datetime64[ms]') # time stamp
#t = np.zeros(nlines,'f')
ax = np.zeros(nlines) # x acceleration
ay = np.zeros(nlines) # y acceleration
az = np.zeros(nlines) # z acceleration
tms = np.zeros(nlines)

# read in data file
infile1 = open(args.datfile,'r')
i = 0
for line in infile1:
    if line.find('Hello') > -1:
        continue
    if line.find('light') > -1:
        continue
    if len(line) < 20: # skip blank lines
        continue
    f = line.split(',')
    #print f
    if len(f) < 4: #skip partial lines
        continue
    
    tms[i] = float(f[0])
    t2=f[2].strip("\"").split()
    #print t2
    #time=dt[1].split(':')
    t[i] = dateutil.parser.parse(t2[1])#, '%H:%M:%S:%f')
    #t[i] = float(time[0])+float(time[1])/60.+float(time[2])/3600.
    ax[i] = float(f[3])
    ay[i] = float(f[4])
    az[i] = float(f[5].strip().rstrip())
    i += 1

infile1.close()

# convert acceleration to m/s^2
range=2. # range of accelerometer in +/- __ G
nbits = 14
g = 9.8 # acceleration of gravity in m/s^2
astep = (range*g/(2**(nbits-1)))
ax = ax*astep
ay = ay*astep
az = az*astep         


deltat = np.array((tms - tms[0]),'f')/1000.

keepflag = (deltat > 0.) 
ax=ax[keepflag]
ay=ay[keepflag]
az=az[keepflag]
deltat = deltat[keepflag]
tms = tms[keepflag]

t = t[keepflag]

freqx, powerx = LombScargle(deltat,ax).autopower()
freqy, powery = LombScargle(deltat,ay).autopower()
freqz, powerz = LombScargle(deltat,az).autopower()

# write out data as csv?
alldat = np.zeros((sum(keepflag),3))
alldat[:,0] = ax
alldat[:,1] = ay
alldat[:,2] = az

#plott=t.astype(dt.datetime)
plott= deltat
#outfile = open(datfile+'.csv','w')
np.savetxt(args.datfile+'-accel.csv',alldat,fmt='%.8e',delimiter=',')
np.savetxt(args.datfile+'-time.csv',deltat,fmt='%.6e',delimiter=',')

def plotfigure():
    plt.figure(figsize=(10,6))
    plt.subplots_adjust(hspace=.3,top=.95,left=.1,right=.95)
    plt.subplot(2,1,1)
    xfmt = mdates.DateFormatter('%H:%M:%S')
    plt.gca().xaxis.set_major_formatter(xfmt)

    plt.plot(plott,ax-np.mean(ax),'c',label='ax')#,s=10,c='c',edgecolors='None',label='ax')
    plt.plot(plott,ay-np.mean(ay)+.1,c='orange',label='ay')#,s=10,edgecolors='None',label='ay')
    plt.plot(plott,az-np.mean(az)-.1,c='g',label='az')#,s=10,edgecolors='None',label='az')
    plt.xlabel('$Time$', fontsize=16)
    plt.ylabel('$Acceleration \ (m/s^2) $',fontsize=16)
    plt.legend(loc='upper right',scatterpoints=1)
    #plt.xlim(min(tx),max(tx))
    #plt.ylim(-2,2)
    plt.subplot(2,1,2)
    plt.plot(freqx,(powerx),'c',label='ax')
    plt.plot(freqy,(powery),c='orange',label='ay')#,s=10,edgecolors='None',)
    plt.plot(freqz,(powerz),c='g',label='az')#,s=10,edgecolors='None',label='ax')
    plt.xlabel('$Frequency \ (Hz)$',fontsize=16)
    plt.ylabel('$Power$',fontsize=16)
    plt.xlim(0,250.)
    plt.legend(loc='upper right',scatterpoints=1)
    plt.savefig('acceleration-vs-time.png')

def plotfigure2():
    plt.figure(figsize=(10,6))
    plt.subplots_adjust(hspace=.3,top=.95,left=.1,right=.95)
    plt.subplot(2,1,1)


    plt.plot(plott,ax-np.mean(ax),'c',label='ax')#,s=10,c='c',edgecolors='None',label='ax')
    plt.plot(plott,ay-np.mean(ay)+.1,c='orange',label='ay')#,s=10,edgecolors='None',label='ay')
    plt.plot(plott,az-np.mean(az)-.1,c='g',label='az')#,s=10,edgecolors='None',label='az')
    plt.xlabel('$Time$', fontsize=16)
    plt.ylabel('$Acceleration \ (m/s^2) $',fontsize=16)
    plt.legend(loc='upper right',scatterpoints=1)
    #plt.xlim(min(tx),max(tx))
    #plt.ylim(-2,2)
    plt.subplot(2,1,2)
    plt.plot(freqx,(powerx),'c',label='ax')
    plt.plot(freqy,(powery),c='orange',label='ay')#,s=10,edgecolors='None',)
    plt.plot(freqz,(powerz),c='g',label='az')#,s=10,edgecolors='None',label='ax')
    plt.xlabel('$Frequency \ (Hz)$',fontsize=16)
    plt.ylabel('$Power$',fontsize=16)
    #plt.xlim(0,250.)
    plt.legend(loc='upper right',scatterpoints=1)
    plt.savefig('acceleration-vs-time.png')
if args.plot:
    plotfigure2()
    
    
if args.plotly:


    trace0 = go.Scatter(x=tx,y=ax-np.mean(ax),
                    mode='markers',
                    name='ax',
                    )
    trace1 = go.Scatter(x=ty,y=ay-np.mean(ay),mode='markers',name='ay')
    trace2 = go.Scatter(x=tz,y=az-np.mean(az),mode='markers',name='az')
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
