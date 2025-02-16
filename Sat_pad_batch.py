# Extrapolate a fits image
# Guillaume Richard
# 2024-09-30
#______________________________________________________________________________
#Parameters, change only this block:
#input fit file to process
SatIn=r'D:/Pixinsight/CDK14/Data/NGC4038/SatEd_Calib-2'

#______________________________________________________________________________
# Import astro for fit image format handeling, skimage for Radon transform
import os
from astropy.io import fits
import numpy as np
import cv2 as cv2

pad_radius=20 
threshold=0.01 # consitent with clip sensitivity in Cosmic Clarity
target_fits='.fits'

#______________________________________________________________________________
def target_files(source_dir,target_pattern):
    for filename in os.listdir(source_dir):
        if filename.endswith(target_pattern):
            yield filename
            
#______________________________________________________________________________
for fitin in target_files(SatIn,target_fits):
    # Read the fit
    print("Reading Fit file:",fitin)
    hdulist = fits.open(os.path.join(SatIn,fitin))
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
    padded = cv2.inpaint(im,m2,pad_radius,cv2.INPAINT_TELEA)
    #padded = cv2.inpaint(im,m2,pad_radius,cv2.INPAINT_NS)
    
    #______________________________________________________________________________
    #write to a new fit
    print("Writing fit out...")
    hdu = fits.PrimaryHDU(padded)
    hdulist = fits.HDUList([hdu])
    fitout=os.path.join(SatIn,fitin.replace(target_fits,"_pad"+target_fits))
    hdulist.writeto(fitout)