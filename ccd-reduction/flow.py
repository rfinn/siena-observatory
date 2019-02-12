Requirements
- ccdproc

#### keep in separate routine ######
For solving WCS and making mosaics:
- sextractor
- scamp
- swarp
#####################################

import ccdproc
from ccdproc import ImageFileCollection
# move any bad files to junk


# replace these with real values
rdnoise = 99
gain = 99.

# check theses using 1/28/19 data
ccdkeyword={'light':'Light Frame','dark':'Dark Frame','flat'='Flat Field','bias':'Bias Frame'}

# make an image collection of all the files in the data directory
ic = ImageFileCollection(os.getcwd(),keywords='*',glob_include='z*.fits')

# select all files with imagetyp=='bias'
bias_files = ic.summary['imagetyp' == 'Light Frame']
# feed list into ccdproc.combine, output bias

zeros = ccdproc.combine(bias_files,method='average',sigma_clip=True,unit=u.adu)
print('writing fits')
zeros.write('bias-combined.fits',overwrite=True)


# select all files with imagetyp=='dark'

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
