# Extrapolate a fits image
# Guillaume Richard
# 2024-09-30
#______________________________________________________________________________
#Parameters, change only this block:
#input fit file to process
fitin=r'D:\Pixinsight\CDK14\Processing\Squid\03_Mosaic\OIII\OIII_starless_clean_DBE.fit'
fitout=r'D:\Pixinsight\CDK14\Processing\Squid\03_Mosaic\OIII\OIII_feather_pad_1001.fit'
#______________________________________________________________________________
# Import astro for fit image format handeling, skimage for Radon transform
from astropy.io import fits
import numpy as np
import cv2 as cv2

blur_radius=1001 # Needs to be odd
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

kernela = np.ones((7,7), np.uint8)
m2= cv2.dilate(m1, kernela) # catch and remove isolated 0 pixels in image area

kernelb = np.ones((blur_radius,blur_radius), np.uint8)
m3= cv2.erode(m2, kernelb)  # do the big regression of the image

m4  = cv2.blur(m3,(blur_radius,blur_radius)) # do a linear decrease of the mask at the edges
bg = m4.astype('float') / 255. #go back to float

#______________________________________________________________________________
# fill all with noise, taken from a place in the image with no data 
noise=im[14200:16362,17226:21330].flatten() # slect an area of pure noise and flatten the array
noisepix= lambda t: np.random.choice(noise) # pick a value at random from the noise area
padding=np.vectorize(noisepix)(im) # fill a new image with noise everywhere

#______________________________________________________________________________
# Smooth merge of image and padding
padded  = im * bg  + padding * (1.0 - bg) # Linear combination of noise and data

#______________________________________________________________________________
#write to a new fit
print("Writing fit out...")
hdu = fits.PrimaryHDU(padded)
hdulist = fits.HDUList([hdu])
hdulist.writeto(fitout)