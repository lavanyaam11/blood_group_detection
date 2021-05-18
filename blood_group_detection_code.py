import numpy as np
from PIL import Image
import cv2
img2 = cv2.imread("input_images\AB.jpeg")
#display input slide
cv2.imshow('slide',img2)
cv2.waitKey(0)
#color plane extraction (green plane extraction)
green_channel = img2[:,:,1]
#binary conversion
ret, thresh1 = cv2.threshold(green_channel,120,255,cv2.THRESH_BINARY)
#inversion
im_ivt= cv2.bitwise_not(thresh1)
cv2.imwrite('inverted.jpg',im_ivt)
im = cv2.imread("inverted.jpg")
#column-wise split - group A, group B, group Rh
height, width, channels = im.shape
width_cutoff = width // 3
sA = im[:,:width_cutoff]
sB = im[:,width_cutoff+1:2*width_cutoff]
sRh = im[:,int(2*width_cutoff)+1:]
#canny edge detection
eA = cv2.Canny(sA,30,300)
eB = cv2.Canny(sB,30,300)
eRh = cv2.Canny(sRh,30,300)
cv2.imshow('canny edges A',eA)
cv2.imshow('canny edges B',eB)
cv2.imshow('canny edges Rh',eRh)
cv2.waitKey(0)
#counting objects (closed edges which can represent agglutinated clump)
cA, hierarchy = cv2.findContours(eA.copy(), cv2.RETR_EXTERNAL,
cv2.CHAIN_APPROX_NONE)
cB, hierarchy = cv2.findContours(eB.copy(), cv2.RETR_EXTERNAL,
cv2.CHAIN_APPROX_NONE)
cRh, hierarchy = cv2.findContours(eRh.copy(), cv2.RETR_EXTERNAL,
cv2.CHAIN_APPROX_NONE)
nA=len(cA)
nB=len(cB)
nRh=len(cRh)
print("The number of objects in the canny edges of A image:",str(nA))
print("The number of objects in the canny edges of B image:",str(nB))
print("The number of objects in the canny edges of Rh image:",str(nRh))
#blood group detection (considering 32 arbitrarily referring the research document)
nA=1 if nA>32 else 0
nB=1 if nB>32 else 0
nRh=1 if nRh>32 else 0
if nA==1:
    if nB==1:
        if nRh==1:
            print("Blood Type: AB+")
        else:
            print("Blood Type:AB-")
    else:
        if nRh==1:
            print("Blood Type: A+")
        else:
            print("Blood Type:A-")
else:
    if nB==1:
        if nRh==1:
            print("Blood Type:B+")
        else:
            print("Blood Type:B-")
    else:
        if nRh==1:
            print("Blood Type:O+")
        else:
            print("Blood Type:O-")
