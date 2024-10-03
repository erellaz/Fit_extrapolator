# Fit extrapolator

## Purpose: 
Get an astonomical image, in fit (fits) format and extrapolate (also: in-paint, pad, noise generate) the no data area.

## Example of application: 
An astronomical image mosaic is created in Ha, SII and OIII. However, only a few tiles have OIII signal. Then only those tiles with signal are acquired. Now the 3 channels (Ha, SII and OIII) have inconsitent data support in the final mosaic. To make a color mosaic through the usual channel combination, the data support of all channels need to be extended, so they are exactly overlapping. Therefore the no data area (here in the OIII channel) needs to be infilled (aka: padded, extrapolated, filled with random noise). The filling needs to be background noise, with statistical properties matching exactly  the statistical properties of actual image in the area where no signal is present. Then the transition between the padding and the actual data tyle needs to be blended (aka: feathered, transitionned) without a visible hard bounday.

## Methodology
Input image is stretched, and has the stars removed. It also has no gradient, or has gone through a gradient removal process. This images has data areas and areas with no data, where the samples are 0, or below a cretain low threshold. The no data areas will be padded. Fit is also single channel.
An area of the image with noise only is selected. Then a new image of the same size as the original is filled with samples randomly selected from the noise area of the original.
Then a mask is created, 0.0 if no data, 1.0 if data. The mask is dilated to protect from dead pixels and make it convex. Then the mask is eroded with a linear ramp.
Then the noise and the original image are linearly combined, using the mask. In the no data area, we get 100% of the noise, in the image area, away from the border we get 100% of the original image, at the boudary we get a linear blend of the noise and the image.

![image](https://github.com/user-attachments/assets/00d09269-7973-42a5-b209-2cfd9e2eba50)
