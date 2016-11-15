#!/usr/bin/python

import numpy as np
import libtiff as tf
import time as tm
from operator import add

import geo

fdir = "layers/"
tdir = "geometry/"
fname = "cellsN8R"

# time the code
t1 = tm.time()

# get the reduced image stack
print "load image stack"
f = tf.TIFF3D.open(fdir+fname+".tif", mode='r') 
images = f.read_image()    # load the image stack
f.close()
xsize = images.shape[1]     # side dimension of images
ysize = images.shape[2]
print "  image grid:", images.shape

# replace grey-scale values with cell number 1-7, empty space = 0
# HARD CODED GREY-SCALE VALUES !!!!
print "renumber cells"
d = {"0":0, "139":4, "162":2, "175":3, "201":7, "208":6, "222":1, "234":5}
for v in np.nditer(images,  op_flags=['readwrite']): v[...] = d[str(v)]

# add top and bottom empty padding layers (full surround empty space)
print "add padding layers"
temp = np.zeros((1, xsize, ysize), dtype=np.uint8)
images = np.concatenate((temp, images, temp))
zsize = images.shape[0]
print "  voxel grid:", images.shape

# adjacency label and sort
print "adjacency label and sort"
sl = [('label', 'S8'), ('hit', np.int8)] # space point label
slabels = np.zeros((xsize-1,ysize-1,zsize-1), dtype=sl) # space point array
pt = [('label', 'S8'), ('ijk', np.int16, (3))] # point label & coordinates
pnts = np.zeros(xsize*ysize*zsize, dtype=pt) # overkill size
pcnt = 0
for k in range(zsize-1):
  for j in range(ysize-1):
    for i in range(xsize-1):
      p8 = images[k:k+2,j:j+2,i:i+2]  # (2x2x2) voxel kernel
      vals = np.unique(p8) # what cells are in this 8 voxel kernel?
      slabels['label'][i,j,k] = ''.join(map(str,vals))
      if (vals.shape[0] == 1) and (vals[0] == 0): continue # skip empty
      pnts[pcnt] = (''.join(map(str,vals)), (i,j,k)) # store label & point indices
      pcnt += 1
pnts = pnts[0:pcnt]          # downsize array
pnts.sort(order=['label'])   # sort array

# output vtk data files
print "output vtk data files"
current = pnts['label'][0]
lcnt = 0
for i, p in enumerate(pnts):
  if p['label'] == current: lcnt += 1
  else:
    geo.save_vtk(tdir, current, pnts['ijk'][i-lcnt:i], [xsize, ysize,zsize])
    lcnt = 1
    current = p['label']
geo.save_vtk(tdir, current, pnts['ijk'][i-lcnt:i], [xsize, ysize,zsize]) # one more time

# output gmsh geo file
##print "output gmsh geo file"
##geo.save_geo(tdir+"cells.geo", [xsize,ysize,zsize], pnts, slabels)

# execution time
print("%dsec" % (tm.time() - t1))

print

