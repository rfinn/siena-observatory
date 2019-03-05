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
from astropy.nddata import CCDData
import os
from astropy.io import fits
import numpy as np
import astropy.units as u
# move any bad files to junk


zerocombine = 1
runzapcosmic = 0
flatcombine = 0
# replace these with real values
# for Siena SBIG STL-11000M CCD
stl_rdnoise = 13. # e-, rms
stl_gain = .8#e-/ADU unbinned
stl_gain = 1.6#e-/ADU unbinned


gain = stl_gain*u.electron/u.adu
rdnoise = stl_rdnoise*u.electron

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
            crimage = ccdproc.cosmicray_lacosmic(ccd, gain = float(gain.value), readnoise = float(rdnoise.value))
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
    gaincorrected_master_bias = ccdproc.gain_correct(master_bias,gain)
    print('writing fits file for master bias')
    gaincorrected_master_bias.write('bias-combined.fits',overwrite=True)
else:
    print('not combining zeros')
    print('reading in bias-combined.fits instead')
    hdu1 = fits.open('bias-combined.fits')
    gaincorrected_master_bias = CCDData(hdu1[0].data, unit=u.electron)
    hdu1.close()
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
gaincorrected_master_dark = ccdproc.gain_correct(master_dark,gain)
print('writing fits file for master dark')
gaincorrected_master_dark.write('dark-combined.fits',overwrite=True)


'''
* subtract bias from combined dark frames
'''

gaincorrected_master_dark_bias = ccdproc.subtract_bias(gaincorrected_master_dark, gaincorrected_master_bias)

print('runzapcosmic = ',runzapcosmic)
if runzapcosmic:

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
try:
    all_filters.remove('0.0')
except KeyError:
    print('no bias frames found after zapping')
if flatcombine:     
    # loop through filters, combine all the flats in that filter
    for filt in all_filters:
        # get of all flats in this filter
        flat_files = icz.files_filtered(imagetyp = ccdkeyword['flat'], filter = filt) 
        # combine images into one flat
        print('combining flats for filter ',filt)
        master_flat = ccdproc.combine(flat_files,method='median',sigma_clip=True,scale=np.median,unit=u.adu)
        gaincorrected_master_flat = ccdproc.gain_correct(master_flat,gain)
        # subtract bias
        # subtract the scaled dark
        print('subtracting bias and scaled dark from combined flat for filter ',filt)
        master_flat_bias_dark = ccdproc.ccd_process(gaincorrected_master_flat, readnoise=rdnoise, master_bias = gaincorrected_master_bias, dark_frame=gaincorrected_master_dark_bias, exposure_key='exposure', exposure_unit=u.second, dark_scale=True, gain_corrected=True)

        print('writing out combined flat for filter ',filt)
        # write output    
        master_flat_bias_dark.write('flat -'+filt+'.fits',overwrite=True)
else:
    print('skipping flat combine')

#####################################################
###### PROCESS SCIENCE IMAGES
#####################################################
print('\n Processing science frames!!!')
for filt in all_filters:
    sci_files = icz.files_filtered(imagetyp = ccdkeyword['light'], filter = filt) 
    master_flat = 'flat -'+filt+'.fits'
    hdu = fits.open(master_flat)
    gaincorrected_master_flat = CCDData(hdu[0].data, unit=u.electron)
    hdu.close()
    # write out image with prefix 'fdb' for flat, dark, bias corrected
    i=0
    for f in sci_files:
        with fits.open(f) as hdu1:
            print ('working on ',f)
            # convert data to CCDData format and save header
            header = hdu1[0].header
            #ccd = CCDData(hdu1[0].data, unit=u.adu,meta={'exposure':header['exposure']})
            ccd = CCDData(hdu1[0].data, unit=u.adu,meta=header)

            newccd = ccdproc.ccd_process(ccd,error=True, gain=gain, readnoise=rdnoise, master_bias = gaincorrected_master_bias, dark_frame=gaincorrected_master_dark_bias, exposure_key='exposure', exposure_unit=u.second, dark_scale=True,master_flat = gaincorrected_master_flat, gain_corrected=True)
            #newccd = ccdproc.ccd_process(ccd,error=True, gain=gain, readnoise=rdnoise, master_bias = gaincorrected_master_bias,master_flat = gaincorrected_master_flat, dark_frame = gaincorrected_master_dark_bias, exposure_key='exposure', exposure_unit = u.second)
            header['HISTORY'] = 'Processing by ccdproc: bias, dark, flat '
            fits.writeto('fdb'+f,newccd,header, overwrite=True)
            hdu1.close()
    if i > 2:
        break

    
'''
# then move on to running scamp and swarp to solve WCS
# and make mosaics

# let's start 01-28-2019 data 

'''
#####################################################
###### CLEANING UP
#####################################################

if cleanup:
    # moved processed a subdirectory
    dirname = 'PROCESSED'
    prefix = 'fdb'
    if os.path.exists(dirname):
        continue
    else:
        os.mkdir(dirname)
    os.system('mv '+prefix+'*.fit* '+dirname+'/.')

    # move zapped to a subdirectory
    dirname = 'ZAPPED'
    prefix = 'z'
    if os.path.exists(dirname):
        continue
    else:
        os.mkdir(dirname)
    os.system('mv '+prefix+'*.fit* '+dirname+'/.')


    # move originals to subdirectory
    dirname = 'ORIGINALS'
    prefix =''
    if os.path.exists(dirname):
        continue
    else:
        os.mkdir(dirname)
    os.system('mv '+prefix+'*.fit* '+dirname+'/.')
    


