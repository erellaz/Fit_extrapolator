# Extrapolate a fits image
# Guillaume Richard
# 2024-09-30
#______________________________________________________________________________
#Parameters, change only this block:
#input fit file to process
fitin=r'L:\Test\out_no_pad\NGC4038_Blue_180.00_2025-01-02_05-31-46_0019_satellited.fits'
fitout=r'L:\Test\out_no_pad\NGC4038_Blue_180.00_2025-01-02_05-31-46_0019_satellited_padded_telea.fits'
#______________________________________________________________________________
# Import astro for fit image format handeling, skimage for Radon transform
from astropy.io import fits
import numpy as np
import cv2 as cv2
import time

# Delayed start
time.sleep(3600*2)

blur_radius=15 # Needs to be odd
threshold=0.18

#______________________________________________________________________________
# Read the fit
print("Reading Fit file:",fitin)
hdulist = fits.open(fitin)
print("\nBasic Fit file information:")
hdulist.info()
print("\nData size:")

#get the array representing the image
im = hdulist[0].data
hdulist.close()
print("Size of the image",im.shape,"\n")

#______________________________________________________________________________
# Create a mask, 0.0 if no data, 1.0 if data
maskgenerator= lambda t: 0.0 if (t<threshold) else 1.0
mask = np.vectorize(maskgenerator)(im)

m1=cv2.convertScaleAbs(mask, alpha=(255.0)) # Go to 8 bits so the cv2 functions work
m2=255-m1


# 2 different inpaint algorithms:
padded = cv2.inpaint(im,m2,20,cv2.INPAINT_TELEA)
#padded = cv2.inpaint(im,m2,20,cv2.INPAINT_NS)


#attmasked=padded * (1-mask)
#fpadded=im+attmasked

# Converting the mask back to 32 bits to export to fit
#bg = m4.astype('float') / 255. #go back to float



#______________________________________________________________________________
#write to a new fit
print("Writing fit out...")
hdu = fits.PrimaryHDU(padded)
#hdu = fits.PrimaryHDU(bg)
hdulist = fits.HDUList([hdu])
hdulist.writeto(fitout)