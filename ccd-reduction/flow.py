'''
Requirements
- ccdproc

#### keep in separate routine ######
# For solving WCS and making mosaics:
# - sextractor
# - scamp
# - swarp
#####################################



References:
https://media.readthedocs.org/pdf/ccdproc/latest/ccdproc.pdf


testing with data from

/Users/rfinn/Dropbox/Siena/observatory/images/reduced/2018-12-04

and sky flats from

/Users/rfinn/Dropbox/Siena/observatory/images/reduced/2018-12-05

'''

import ccdproc
from ccdproc import ImageFileCollection
import os
from astropy.io import fits
import numpy as np
# move any bad files to junk


zerocombine=0


# replace these with real values
# for Siena SBIG STL-11000M CCD
stl_rdnoise = 13. # e-, rms
stl_gain = .8#e-/ADU unbinned
stl_gain = 1.6#e-/ADU unbinned

# check theses using 1/28/19 data
ccdkeyword={'light':'Light Frame','dark':'Dark Frame','flat':'Flat Field','bias':'Bias Frame'}



def zapcosmic(file_list):
    i=0
    nfiles = len(flat_files)
    for f in file_list:
        print ('ZAPPING COSMIC RAYS FOR FILE %i OF %i'%(i,nfiles))
        with fits.open(f) as hdu1:
            print ('working on ',f)

            # convert data to CCDData format and save header
            ccd = CCDData(hdu1[0].data, unit=u.adu)
            header = hdu1[0].header
            crimage = ccdproc.cosmicray_lacosmic(ccd, gain = float(args.gain), readnoise = float(args.rdnoise))
            header['HISTORY'] = 'Cosmic rays rejected using ccdproc.cosmicray_lacosmic '
            fits.writeto('z'+f,crimage,header)
            hdu1.close()
        i += 1
        print ('\n')

# make an image collection of all the files in the data directory
# z is prefix for galaxies that already have cosmic ray rejection
ic = ImageFileCollection(os.getcwd(),keywords='*',glob_include='*.fit')


# correct for gain


# combine bias frames

if zerocombine:
    # select all files with imagetyp=='bias'
    bias_files = ic.files_filtered(imagetyp = ccdkeyword['bias'])
    # feed list into ccdproc.combine, output bias

    master_bias = ccdproc.combine(bias_files,method='average',sigma_clip=True,unit=u.adu)
    print('writing fits')
    master_bias.write('bias-combined.fits',overwrite=True)

###################################################
# COMBINE DARKS
###################################################
# identify darks and combine darks with longest exposure time


# select all files with imagetyp=='dark'
# want to read in one set of long exposure dark frames, like 120 s
# observers should take a set of darks that correspond to longest exposure time
# e.g. 120s
exptimes = np.array(ic.values('exptime'))
image_types = np.array(ic.values('imagetyp'))

max_exposure = max(exptimes[image_types == ccdkeyword['dark']])



dark_files = ic.files_filtered(imagetyp = ccdkeyword['dark'], exptime = max_exposure)

master_dark = ccdproc.combine(dark_files,method='average',sigma_clip=True,unit=u.adu)
master_dark.write('dark-combined.fits',overwrite=True)


'''
* subtract bias from combined dark frames
'''

master_dark_bias = ccdproc.subtract_bias(master_dark, master_bias)



###################################################
# COSMIC RAY REJECTION
###################################################
# run LA cosmic on flat field images

flat_files = ic.files_filtered(imagetyp = ccdkeyword['flat'])

zapcosmic(flat_files)

# run LA cosmic on science images

sci_files = ic.files_filtered(imagetyp = ccdkeyword['light'])
zapcosmic(sci_files)


# make an image collection of all the files in the data directory
# z is prefix for galaxies that already have cosmic ray rejection
icz = ImageFileCollection(os.getcwd(),keywords='*',glob_include='z*.fit')

filters = icz.values('filter')
image_types = np.array(icz.values('imagetyp'))


#####################################################
###### PROCESS FLAT FIELD IMAGES
#####################################################

# create a set of unique filters
all_filters = set(np.array(filters))
# gets rid of 0.0, which is what the dark 'filter' will come through as
all_filters.remove('0.0')

# loop through filters, combine all the flats in that filter
for filt in all_filters:
    # get of all flats in this filter
    flat_files = icz.files_filtered(imagetyp = ccdkeyword['flat'], filter = filt) 
    # combine images into one flat
    master_flat = ccdproc.combine(flat_files,method='median',sigma_clip=True,scale=np.median,unit=u.adu)

    # subtract bias
    # subtract the scaled dark
    master_flat_bias_dark = ccdproc.ccd_process(master_flat,error=True, gain=stl_gain*u.electron/u.adu, readnoise=stl_readnoise*u.electron, dark_frame=master_dark, exposure_key='exposure', exposure_unit=u.second, dark_scale=True)
    
    # write output    
    master_flat_bias_dark.write('flat -'+filt+'.fits',overwrite=True)


#####################################################
###### PROCESS SCIENCE IMAGES
#####################################################

for filt in all_filters:
    sci_files = icz.files_filtered(imagetyp = ccdkeyword['light'], filter = filt) 
    master_flat = 'flat -'+filt+'.fits'

    # write out image with prefix 'fdb' for flat, dark, bias corrected

    for f in sci_files:
        with fits.open(f) as hdu1:
            print ('working on ',f)
    
            # convert data to CCDData format and save header
            ccd = CCDData(hdu1[0].data, unit=u.adu)
            header = hdu1[0].header
            newccd = ccdproc.ccd_process(f,error=True, gain=stl_gain*u.electron/u.adu, readnoise=stl_readnoise*u.electron, dark_frame=master_dark, exposure_key='exposure', exposure_unit=u.second, dark_scale=True,master_flat = master_flat)
            header['HISTORY'] = 'Processing by ccdproc: bias, dark, flat '
            fits.writeto('fdb'+f,newccd,header)
            hdu1.close()

    
'''
# then move on to running scamp and swarp to solve WCS
# and make mosaics

# let's start 01-28-2019 data 

'''
