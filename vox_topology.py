#!/usr/bin/python

import numpy as np
import libtiff as tf
from pyevtk.hl import pointsToVTK

fdir = "layers/"
tdir = "topology/"
fname = "cellsN2R"

# get the reduced image stack
f1 = tf.TIFF3D.open(fdir+fname+".tif", mode='r') 
images = f1.read_image()    # load the image stack
f1.close()
xsize = images.shape[1]     # side dimension of images
ysize = images.shape[2]

# replace grey-scale values with cell number (for easy identifucation and indexing)
# NOTE: hard-coded values !!!
d = {"0":0, "139":4, "162":2, "175":3, "201":7, "208":6, "222":1, "234":5}
for v in np.nditer(images,  op_flags=['readwrite']):
  v[...] = d[str(v)]

# add top and bottom empty padding layers (for full surround with empty space)
temp = np.zeros((1, xsize, ysize), dtype=np.uint8)
images = np.concatenate((temp, images, temp))
zsize = images.shape[0]
print "\nvoxel grid:"
print ' ', images.shape

# scan for cell edge points
xyz = np.zeros((xsize*ysize, 3), dtype=np.float) # hopefully big enough!!!

pcnt = 0
print "\ncell 1 - edge points:"
for k in range(zsize-1):
  for j in range(ysize-1):
    for i in range(xsize-1):
      p8 = images[k:k+2,j:j+2,i:i+2]
      vals = np.unique(p8)
      if vals.shape[0] > 2:
        #if 1 in p8: 
        print i+1, j+1, k+1, vals
        z = (24.73 / 2) - ((k+2) * 24.73 / zsize)
        x = ((i+1) * 70.66 / xsize) - (70.66 / 2)
        y = (70.66 / 2) - ((j+1) * 70.66 / ysize)
        xyz[pcnt] = (x, y, z)
        pcnt += 1

d = {}
null = np.full(pcnt, 1)
d["null"] = null
pointsToVTK(tdir+fname, xyz[0:pcnt,0], xyz[0:pcnt,1], xyz[0:pcnt,2], d) # write out vtk file

