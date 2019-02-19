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
rdnoise = 99
gain = 99.

# check theses using 1/28/19 data
ccdkeyword={'light':'Light Frame','dark':'Dark Frame','flat':'Flat Field','bias':'Bias Frame'}

# make an image collection of all the files in the data directory
# z is prefix for galaxies that already have cosmic ray rejection
ic = ImageFileCollection(os.getcwd(),keywords='*',glob_include='z*.fits')


# correct for gain


# combine bias frames

if zerocombine:
    # select all files with imagetyp=='bias'
    bias_files = ic.files_filtered(imagetyp = ccdkeyword['bias'])
    # feed list into ccdproc.combine, output bias

    zeros = ccdproc.combine(bias_files,method='average',sigma_clip=True,unit=u.adu)
    print('writing fits')
    zeros.write('bias-combined.fits',overwrite=True)


# identify darks and combine darks with longest exposure time


# select all files with imagetyp=='dark'
# want to read in one set of long exposure dark frames, like 120 s
# observers should take a set of darks that correspond to longest exposure time
# e.g. 120s
exptimes = np.array(ic.values('exptime'))
image_types = np.array(ic.values('imagetyp'))

max_exposure = max(exptimes[image_types == ccdkeyword['dark']])



dark_files = ic.files_filtered(imagetyp = ccdkeyword['dark'], exptime = max_exposure)

dark_combined = ccdproc.combine(dark_files,method='average',sigma_clip=True,unit=u.adu)



'''
Next time

* subtract bias from dark

* subtract bias from science and flat frames

* subtract dark from science and flat frames by scaling bias-subtracted dark

dark_subtracted = ccdproc.subtract_dark(bias_subtracted, master_dark, exposure_time='exposure', exposure_unit=u.second, scale=True)




* combine flats


* correct for gain

gain_correct(ccd, gain, gain_unit=None, add_keyword=True) Correct the gain in the image.



* run science through ccd proc - subtract bias, a scaled dark, and then flaten

nccd = ccdproc.ccd_process(ccd, oscan='[201:232,1:100]',
... trim='[1:200, 1:100]',
... error=True,
... gain=2.0*u.electron/u.adu,
... readnoise=5*u.electron,
... dark_frame=master_dark,
... exposure_key='exposure',
... exposure_unit=u.second,
... dark_scale=True,
... master_flat=master_flat)


'''

'''
# feed list into ccdproc.combine, output dark



# combine darks with long exposure time


## make flats
# select all files with imagetyp=='flat'

# combine all flats in the same filter

t = ic2.summary['filter']
filter_list = set(t)

then loop over filter_list

make filelist with filter=f, imagetyp='flat'

combine files in list


# process science frames
loop over filters:

select images with   filter=f, imagetyp='light'
    fileset = ic.files_filtered(filter='Red',exptime=30.000,imagetyp=ccdkeyword['light'])
    ccdproc( bias+, dark+, flat+)


# then move on to running scamp and swarp to solve WCS
# and make mosaics

# let's start 01-28-2019 data 

'''
