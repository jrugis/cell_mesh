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
print "  image grid:", images.shape

# replace grey-scale values with cell number 1-7, empty space = 0
### NOTE: FROM HARD CODED GREY-SCALE VALUES ###
print "renumber cells"
d = {"0":0, "139":4, "162":2, "175":3, "201":7, "208":6, "222":1, "234":5}
for v in np.nditer(images,  op_flags=['readwrite']): v[...] = d[str(v)]

# add top and bottom empty padding layers (full surround empty space)
print "add padding layers and swap axes"
temp = np.zeros((1, images.shape[1], images.shape[2]), dtype=np.uint8)
voxels = np.swapaxes(np.concatenate((temp, images, temp)), 0, 2) # reorder to z-stack
print "  voxel grid:", voxels.shape

# label line segments
print "label line segments"
sl = [('xyzlabel', 'S8', 3), ('xyzhit', np.bool, 3), ('endp', np.bool)]
slabels = np.zeros(voxels.shape, dtype=sl) # space point xyz label array
print ' ', geo.line_segs(voxels, slabels)

# cull singletons
print "cull singletons"
while True:
  culled = geo.line_cull(slabels)
  print ' ', culled
  if culled == 0: break
  
# locate end points
print "locate end points"
print ' ', geo.end_points(slabels)

# save cgal ploylines file
print "save cgal polylines file"
geo.save_polylines(tdir+fname, slabels)

# view line segments
##print "view line segments"
##geo.view_lsegs(slabels)

# execution time
print("%d seconds" % (tm.time() - t1))

print

