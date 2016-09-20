#!/usr/bin/python

import numpy as np
import libtiff as tf
from pyevtk.hl import pointsToVTK

fdir = "layers/"
tdir = "geometry/"
fname = "cellsN8R"

# save geometryy files
def save_geom(label, pnts):
  n = pnts.shape[0]
  print("  label:%-4s count:%i"% (label, n))
  np.savetxt(tdir+'geom_'+label+".dat", pnts, fmt='%2.4f') # text file
  d = {}                                      # vtk file
  null = np.full(n, 0.0)                      #
  d["null"] = null                            #    
  pointsToVTK(tdir+'geom_'+label, pnts[:,0], pnts[:,1], pnts[:,2], d)
  return

# get the reduced image stack
print "load image stack"
f1 = tf.TIFF3D.open(fdir+fname+".tif", mode='r') 
images = f1.read_image()    # load the image stack
f1.close()
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
pt = [('label', 'S12'), ('xyz', np.float, (3))] # topology label & point coordinates
pnts = np.zeros(xsize*ysize*zsize, dtype=pt) # overkill size
pcnt = 0
for k in range(zsize-1):
  for j in range(ysize-1):
    for i in range(xsize-1):
      p8 = images[k:k+2,j:j+2,i:i+2]  # (2x2x2) voxel kernel
      vals = np.unique(p8)            # what cells are in this 8 voxel kernel?
      if (vals.shape[0] == 1) and (vals[0] == 0): continue # skip empty
      z = (24.73 / 2) - ((k+1) * 24.73 / (zsize-2))  # calculate 3D point coordinates
      x = ((i) * 70.66 / xsize) - (70.66 / 2)
      y = (70.66 / 2) - ((j) * 70.66 / ysize)
      pnts[pcnt] = (''.join(map(str,vals)), (x,y,z)) # store label & point coordinates
      pcnt += 1
pnts = pnts[0:pcnt]          # downsize array
pnts.sort(order=['label'])   # sort array

# output geometry files
print "output geometry files"
current = pnts['label'][0]
lcnt = 0
for i, p in enumerate(pnts):
  if p['label'] == current: lcnt += 1
  else:
    save_geom(current, pnts['xyz'][i-lcnt:i])
    lcnt = 1
    current = p['label']
save_geom(current, pnts['xyz'][i-lcnt:i]) # one more time

print

