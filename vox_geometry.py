#!/usr/bin/python

import numpy as np
import libtiff as tf
from operator import add
from pyevtk.hl import pointsToVTK
from mayavi.mlab import *

fdir = "layers/"
tdir = "geometry/"
fname = "cellsN8R"

# recursively find next point on line
def next_point(slabels, ijk, end_label, line_label, llist):
  llist.append(ijk)
  slabels['hit'][tuple(ijk)] = 1 # mark space point as hit
  adj = [[-1,0,0],[1,0,0],[0,-1,0],[0,1,0],[0,0,-1],[0,0,1]]
  for n in range(len(adj)): # scan adjacent points
    t = map(add, ijk, adj[n])
    if (slabels['hit'][tuple(t)] != 1): # already hit?
      l = slabels['label'][tuple(t)]
      if (l == line_label) or (l == end_label): # on the line?
        next_point(slabels, t, end_label, line_label, llist) # keep going
  return

# indices to coordinates
def i2xyz(ijk, size):
  x = ((ijk[0]) * 70.66 / size[0]) - (70.66 / 2)
  y = (70.66 / 2) - ((ijk[1]) * 70.66 / size[1])
  z = (24.73 / 2) - ((ijk[2]+1) * 24.73 / (size[2]-2))
  return np.array([x,y,z])

# save geometry files
def save_geom(label, pnts, size):
  n = pnts.shape[0]
  print("  label:%-4s count:%i"% (label, n))
  xyz = np.zeros((n,3), dtype=np.float)
  for i, p in enumerate(pnts):
    xyz[i] = i2xyz(p, size)
  np.savetxt(tdir+'geom_'+label+".dat", xyz, fmt='%2.4f') # text file
  d = {}                                      # vtk file
  null = np.full(n, 0.0)                      #
  d["null"] = null                            #    
  pointsToVTK(tdir+'geom_'+label, xyz[:,0], xyz[:,1], xyz[:,2], d)
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
sl = [('label', 'S8'), ('hit', np.int8)] # space point label
slabels = np.zeros((xsize-1,ysize-1,zsize-1), dtype=sl) # space point array
pt = [('label', 'S8'), ('ijk', np.int16, (3))] # point label & coordinates
pnts = np.zeros(xsize*ysize*zsize, dtype=pt) # overkill size
pcnt = 0
for k in range(zsize-1):
  for j in range(ysize-1):
    for i in range(xsize-1):
      p8 = images[k:k+2,j:j+2,i:i+2]  # (2x2x2) voxel kernel
      vals = np.unique(p8)            # what cells are in this 8 voxel kernel?
      slabels['label'][i,j,k] = ''.join(map(str,vals))
      if (vals.shape[0] == 1) and (vals[0] == 0): continue # skip empty
      pnts[pcnt] = (''.join(map(str,vals)), (i,j,k)) # store label & point indices
      pcnt += 1
pnts = pnts[0:pcnt]          # downsize array
pnts.sort(order=['label'])   # sort array

# output geometry data files
print "output geometry data files"
current = pnts['label'][0]
lcnt = 0
for i, p in enumerate(pnts):
  if p['label'] == current: lcnt += 1
  else:
    save_geom(current, pnts['ijk'][i-lcnt:i], [xsize, ysize,zsize])
    lcnt = 1
    current = p['label']
save_geom(current, pnts['ijk'][i-lcnt:i], [xsize, ysize,zsize]) # one more time

# get ordered line point list
end_label = "0567"
line_label = "567"
print("line walk: %s-%s-%s"% (end_label, line_label, end_label))
llist = []
ijk = pnts['ijk'][np.where(pnts['label']==end_label)[0][0]].tolist()
next_point(slabels, ijk, end_label, line_label, llist)
print llist

# plot the line
llist = np.array(llist)
plot3d(llist[:,0],llist[:,1],llist[:,2], tube_radius=0.1, color=(1,0,0))
show()

print

