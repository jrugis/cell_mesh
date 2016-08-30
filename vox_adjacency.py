#!/bin/bash

import numpy as np
import libtiff as tf

fdir = "layers/"
fname = "cellsNR"

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
print images.shape

# probe cell adjacency
cnts = np.zeros((8, 8), dtype=np.uint16) # adjacency counts matrix
vals = np.zeros((7), dtype=np.uint8)  # temp: voxel neighbor values
cvs = np.unique(images)
for cv in cvs[1:]:
  xyz = np.where(images == cv)
  z = xyz[0]
  x = xyz[2]
  y = xyz[1]
  print cv, x.shape[0]
  for i in range(x.shape[0]):
    vals[0] = images[z[i]  , y[i]  , x[i]  ]
    vals[1] = images[z[i]  , y[i]  , x[i]+1]
    vals[2] = images[z[i]  , y[i]  , x[i]-1]
    vals[3] = images[z[i]  , y[i]+1, x[i]  ]
    vals[4] = images[z[i]  , y[i]-1, x[i]  ]
    vals[5] = images[z[i]+1, y[i]  , x[i]  ]
    vals[6] = images[z[i]-1, y[i]  , x[i]  ]
    for j in range(1, vals.shape[0]):
      if vals[j] != vals[0]:
        cnts[vals[0], vals[j]] += 1

print cnts[1:] # adjacency matrix



