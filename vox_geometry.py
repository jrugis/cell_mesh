#!/usr/bin/python

import numpy as np
import libtiff as tf
import time as tm
from operator import add

import geo
import poly
import vis

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
print "label line segments (first pass)"
sl = [('xyzlabel', 'S8', 3), ('xyzhit', np.bool, 3), ('endp', np.bool)]
slabels = np.zeros(voxels.shape, dtype=sl) # space point xyz label array
total_segments = geo.line_segs(voxels, slabels)
print ' ', total_segments, "segments (raw)"

# cull singletons
print "cull singleton line segments"
total_culled = 0
while True:
  culled = geo.line_cull(slabels)
  print ' ', culled, "culled"
  total_culled += culled
  if culled == 0: break
  
# flag end points
print "flag end points"
print ' ', geo.end_points(slabels), "points"

#### temp vis for debug ###
print "view end points and line segments"
vis.view_lsegs(slabels)

# get line geometry
print "get line geometry"
lines = geo.get_lines(slabels) # returns a list of point lists
print ' ', len(lines), "lines"

# check line segment coverage
print "check line segment coverage"
segment_coverage = geo.check_lsegs(slabels)
print ' ', segment_coverage, "segments"
if segment_coverage != total_segments - total_culled:
  print "  ERROR: total segment count mismatch"
  print "  NOTE: possible line loop (line without endpoints)" 

# save polylines file
print "save polylines file"
poly.save_poly(tdir+fname, lines)

# execution time
print("%d seconds" % (tm.time() - t1))

print

