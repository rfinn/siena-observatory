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
#import dateutil.parser
import datetime as dt

from astropy.stats import LombScargle
import matplotlib
#matplotlib.use('WXAgg')
matplotlib.use('TkAgg')

import matplotlib.dates as mdates
from matplotlib import pyplot as plt
from datetime import datetime
import pandas as pd
import util


parser = argparse.ArgumentParser(description = 'This code creates a csv file and plots data from accelerometer.  Data file is generated from readAcceleration.py.  An example of running the code from the command line is:   python plotData.py --datfile junk-2017Mar25 --plot')
parser.add_argument('--datfile', dest = 'datfile', default='fake_data',help = 'filename that contains data from accelerometer.  default is junk-2017Mar25')
parser.add_argument('--plot', dest = 'plot', default = False, action = 'store_true', help = 'generate plot of acceleration data and FFT using matplotlib.  Figure is saved as acceleration-vs-time.png.  default is False.')
parser.add_argument('--plotly', dest = 'plotly', default = False, action = 'store_true', help = 'generate plot of acceleration data on plotly.  default is False.  ')
parser.add_argument('--fourier', dest = 'fourier', default = False, action = 'store_true', help = 'Calculate fourier transform.  default is False.  ')
parser.add_argument('--makecsv', dest = 'makecsv', default = False, action = 'store_true', help = 'Convert data files to CSV format')

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


def calcfft():

    freqx, powerx = LombScargle(deltat,ax).autopower()
    freqy, powery = LombScargle(deltat,ay).autopower()
    freqz, powerz = LombScargle(deltat,az).autopower()
    print '  done with that'
    plt.figure()
    plt.plot(freqx,(powerx),'c',label='ax',lw=.5) # apparently lw<1 plots faster
    plt.plot(freqy,(powery),c='orange',label='ay',lw=.5)#,s=10,edgecolors='None',)
    plt.plot(freqz,(powerz),c='g',label='az',lw=.5)#,s=10,edgecolors='None',label='ax')
    plt.xlabel('$Frequency \ (Hz)$',fontsize=16)
    plt.ylabel('$Power$',fontsize=16)
    plt.xlim(0,120)
    plt.savefig(args.datfile+'fft.png')

def getoutlier(y,sigma=4,grow=100):
    noise = np.std(y)
    eventflag = abs(y-np.mean(y)) > sigma*noise
    ievent = np.arange(len(y))[eventflag]
    for i in ievent:
        #check if i < 100:
        if i < grow:
            eventflag[0:i+grow]=np.ones((i+grow),'bool')
        elif (i+grow) > len(eventflag):
            eventflag[i-grow:len(eventflag)-1]=np.ones(len(eventflag)-i-grow,'bool')
        else:
            eventflag[i-grow:i+grow]=np.ones(2*grow,'bool')
    # find first part of a given event
    diff = np.zeros(len(eventflag)-1)
    diff = np.array(eventflag[0:-1],'i') - np.array(eventflag[1:],'i')
    #print diff[0:30]
    startevent = ievent[1:-1][diff == -1]
    return startevent,eventflag,diff
    
def plotfigure(usehexbin=False,binsize=.01,ymin=-.15,ymax=.15,dytick=.1,nhexbin=10):
    xdim=16
    ydim=4
    plt.figure(figsize=(xdim,ydim))
    plt.subplots_adjust(hspace=.0,left=.075,right=.95,bottom=.15,top=.9)
    datapts=[ax,ay,az]
    datapts2=[ax,ay,az]
    ylabels=['$\Delta a_x$','$\Delta a_y$','$\Delta a_z$']

    colors=['c','orange','g']
    #ymin=-.3
    #ymax=.3
    #dytick=.2
    
    for i in range(len(datapts)):
        
        plt.subplot(3,1,i+1)
        y=datapts[i]-np.mean(datapts[i])
        if usehexbin:
            plt.hexbin(t,y,gridsize=(nhexbin*xdim,nhexbin*ydim),cmap='gray_r')#,marker='.')#,s=10,c='c',edgecolors='None',label='ax')
        else:
            plt.plot(t,y,colors[i],label='ax',rasterized=True,lw=.05)#,marker='.')#,s=10,c='c',edgecolors='None',label='ax')
        bins,stats= util.medxbin(t,y,binsize)
        plt.ylabel(ylabels[i],fontsize=16)
        plt.plot(bins,stats['median'],'r-',lw=2)
        plt.plot(bins,stats['median']+.5*stats['iqr'],'r-',lw=.5)
        plt.plot(bins,stats['median']-.5*stats['iqr'],'r-',lw=.5)
        if i < 2:
            plt.xticks([])
        if i == 0:
            plt.title(args.datfile)
        if np.mean(datapts[i]) > 7.:
            plt.text(.05,.85,'vertical direction',transform=plt.gca().transAxes,horizontalalignment='left')
        plt.text(.9,.85,'std = %.5f'%(np.std(y)),transform=plt.gca().transAxes,horizontalalignment='right')
        plt.yticks(np.arange(int(ymin*10)/10,(ymax)+dytick,dytick))
        plt.axhline(y=0,ls='-',color='k')
        plt.ylim(ymin,ymax)
    plt.xlabel('$Time \ (hr)$', fontsize=16)


    #plt.ylabel('$Acceleration \ (m/s^2) $',fontsize=16)
    #plt.legend(loc='upper right',scatterpoints=1)
    #plt.xlim(min(tx),max(tx))
    #plt.ylim(-2,2)

    #plt.xlim(0,250.)
    #plt.legend(loc='upper right',scatterpoints=1)
    if usehexbin:
        plt.savefig('plots/'+args.datfile+'-avst-hexbin.png')
    else:
        plt.savefig('plots/'+args.datfile+'-avst.png')

def plotfigure2():
    plt.figure(figsize=(10,6))
    #plt.subplots_adjust(hspace=.3,top=.95,left=.1,right=.95)
    #plt.subplot(2,1,1)


    plt.plot(plott,ax-np.mean(ax),'c',label='ax',lw=.5)#,s=10,c='c',edgecolors='None',label='ax')
    plt.plot(plott,ay-np.mean(ay)+.1,c='orange',label='ay',lw=.5)#,s=10,edgecolors='None',label='ay')
    plt.plot(plott,az-np.mean(az)-.1,c='g',label='az',lw=.5)#,s=10,edgecolors='None',label='az')
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
    plt.ylim(-.2,.2)
    plt.legend(loc='upper right',scatterpoints=1)
    plt.savefig('acceleration-vs-time.png')


'''
infile1 = open(args.datfile,'r')
nlines=len(infile1.readlines())
infile1.close()
print 'number of data points = ',nlines
nlines = nlines #-1
# set up data arrays
t = np.zeros(nlines,dtype='datetime64[ms]') # time stamp
#t = np.zeros(nlines,'f')
ax = np.zeros(nlines) # x acceleration
ay = np.zeros(nlines) # y acceleration
az = np.zeros(nlines) # z acceleration
tms = np.zeros(nlines)

startTime = datetime.now()
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
    f = line.split()
    #print f
    if len(f) < 4: #skip partial lines
        continue
    
    
    t[i] = dateutil.parser.parse(f[0])#, '%H:%M:%S:%f')
    #t[i] = float(time[0])+float(time[1])/60.+float(time[2])/3600.
    ax[i] = float(f[1])
    ay[i] = float(f[2])
    az[i] = float(f[3].strip().rstrip())
    i += 1

infile1.close()
print 'done reading data file'
endTime = datetime.now()
print 'delta T =',endTime-startTime

#print 'comparing with loadtxt'

#dat = np.loadtxt(args.datfile,converters = {0: mdates.datestr2num})
'''
t3=datetime.now()
#print 'delta T =', t3- endTime

rpi1 = False # for Michele's accelerometer
#print 'comparing with loadtxt, skipping time column'
if rpi1:
    dat = np.loadtxt(args.datfile,dtype='S16,f,f,f,f,f,f',unpack=True)
    t4=datetime.now()
    print 'delta T =', t4-t3
    print 'reading times'
    #newtime=dat[0]
    hr = np.array([u[0:2] for u in dat[0]],'f')

    mm = np.array([u[3:5] for u in dat[0]],'f')
    ss = np.array([u[6:15] for u in dat[0]],'f')
    dectime = hr+mm/60.+ss/3600.
    ax=dat[1]
    ay=dat[2]
    az=dat[3]
    ax2=dat[4]
    ay2=dat[5]
    az2=dat[6]
    t5=datetime.now()
    print 'finish converting time to array delta T =', t5-t4
else:
    dat = np.genfromtxt(args.datfile,skip_footer=1)
    t4=datetime.now()
    print 'delta T =', t4-t3
    print 'reading times'

    dectime = (dat[:,0]-dat[:,0][0])/3600. # hrs
    ax=dat[:,1]*9.8# data are in units of g
    ay=dat[:,2]*9.8
    az=dat[:,3]*9.8
## # convert acceleration to m/s^2
## range=2. # range of accelerometer in +/- __ G
## nbits = 14
## g = 9.8 # acceleration of gravity in m/s^2
## astep = (range*g/(2**(nbits-1)))
## ax = ax*astep
## ay = ay*astep
## az = az*astep   



deltat = np.array((dectime - dectime[0]),'f')*3600 # in seconds #/1000.

keepflag = (deltat > 0.) 
ax=ax[keepflag]
ay=ay[keepflag]
az=az[keepflag]
deltat = deltat[keepflag]
#tms = tms[keepflag]

t = dectime[keepflag]
plott= deltat
if args.makecsv:
    # write out data as csv?
    alldat = np.zeros((sum(keepflag),3))
    alldat[:,0] = ax
    alldat[:,1] = ay
    alldat[:,2] = az

    #plott=t.astype(dt.datetime)

    #outfile = open(datfile+'.csv','w')
    np.savetxt(args.datfile+'-accel.csv',alldat,fmt='%.8e',delimiter=',')
    np.savetxt(args.datfile+'-time.csv',deltat,fmt='%.6e',delimiter=',')

if args.plot:
    plotfigure()
    plotfigure(usehexbin=True)
    
if args.fourier:
    print 'calculating fourier transform'
    calcfft()
    
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
