# -*- coding: utf-8 -*-

import numpy as np
import cv2
from matplotlib import pyplot as plt
import math
import scipy
from scipy import signal
from PIL import Image
from skimage.feature import peak_local_max, canny
from scipy import ndimage as ndi


def LocalMaximaChecker(voting, foundmaxima, i,j,accumulator, width, height, ranx, rany):
        
        for x in ranx:
            for y in rany:
                if   x > 0 and y > 0 and x <width and y <height:
                    if voting[i][j].max() < voting[x][y].max() or accumulator [x][y] > 0:
                        foundmaxima = 1
                        break
            if foundmaxima==1:
                break
        return foundmaxima                                                             
im=Image.open('HoughCircles.jpg').convert('L')
dia=np.shape(im)
maxdia=np.max(dia)
maxdia=maxdia/8
mindia=np.min(dia)
mindia=mindia/8
im1=Image.open('HoughCircles.jpg')
pixels=np.array(im)
im2=np.array(im1)
kernel = np.ones((5,5))
Eroded = cv2.erode(pixels,kernel,iterations=5)
cv2.imwrite('erosion.jpg', Eroded)
Dilated = cv2.dilate(Eroded,kernel,iterations=5)
cv2.imwrite('dilation.jpg', Dilated)
Blurred = ndi.filters.gaussian_filter(Dilated,3.0)
cv2.imwrite('blurred.jpg', Blurred)
edges = canny(Blurred, sigma=3, low_threshold=10, high_threshold=27)

x,y=edges.shape

edge_matrix=np.zeros((x,y))
edgePts = []
for i in range(0,x):
    for j in range(0,y):
        if (edges[i][j]==True):
            edge_matrix[i][j]=255
            edgePts.append((i,j))
        else:
            edge_matrix[i][j]=0

temp1,temp2=np.shape(edgePts)
cv2.imwrite('edgematrix.jpg', edge_matrix)
numOfEdge = temp1
MinR=26
MaxR=MinR+3
radius_range=[MinR, MaxR]
startr=0
accumulator = np.zeros((x,y))
voting=np.zeros((x,y,radius_range[1]))
set_threshold = 52
center_coord = list()
cntr=0
k=0
#begin detection: Hough Transform
for each in range(0, maxdia):
    if k!=0:
        radius_range[1]+=1
     
    for i in range(0, numOfEdge):
      
        for r in range(radius_range[0],radius_range[1]):
        
            for theta in range(0,360, 5):
                a=edgePts[i][0]-startr*math.cos(theta*math.pi/180)
                b=edgePts[i][1]-startr*math.sin(theta*math.pi/180)
    
                if a>0 and a<x:
                    
                    if b>0 and b<y:
                        
                        voting[a,b,startr]+=1
        startr=(r-radius_range[0])/5+radius_range[0]

    max_prior=0
    
    for i in range(0,x):
        for j in range(0,y):
            if edge_matrix[i][j]==0 and voting[i][j].max()>set_threshold:
                range_x = np.arange(i-22, i+22,1)
                range_y = np.arange(j-22, j+22,1)
                if not LocalMaximaChecker(voting,max_prior, i,j,accumulator,x,y, range_x, range_y):
                    accumulator[i][j]=r
                    tmp_list=[i,j,r]
                    center_coord.append(tmp_list)
                    
    radius_range[0]=radius_range[1]+1
    radius_range[1]+=2
    k+=1
    if radius_range[1]>maxdia:
        break
    else:
        
        voting=np.zeros((x,y,radius_range[1]))


########################Drawing the circle


Radius = [row[-1] for row in center_coord]
for i in range(0, len(Radius)):

    for theta in range(0, 360):
        
        a = center_coord[i][0]-Radius[i]*math.cos(theta*math.pi/180)
        b = center_coord[i][1]-Radius[i]*math.sin(theta*math.pi/180)
        #all within the set of dimensions of image
        if a > 0 and b > 0 and a <x and b <y:
            im2[a,b,0]=255
            im2[a,b,1]=100
            im2[a,b,2]=200
            #edge_matrix[a,b]=255
      
cv2.imshow('image',im2)  

fig, ( ax2) = plt.subplots(nrows=1, ncols=1, figsize=(8, 3), sharex=True, sharey=True)

ax2.imshow(edge_matrix, cmap=plt.cm.gray)
ax2.axis('off')
ax2.set_title('Canny filter, $\sigma=3$', fontsize=20)

fig.subplots_adjust(wspace=0.02, hspace=0.02, top=0.9,
                    bottom=0.02, left=0.02, right=0.98)

plt.show()
