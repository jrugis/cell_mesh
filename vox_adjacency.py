#!/usr/bin/python

import numpy as np
import libtiff as tf

fdir = "layers/"
fname = "cellsN16R"

def write_msh(xsize, ysize, zsize, quads):
  qsize = quads.shape
  f1 = open("bounding.msh", "w")
  f1.write("$MeshFormat\n")
  f1.write("2.2 0 8\n")
  f1.write("$EndMeshFormat\n")

  f1.write("$Nodes\n")
  f1.write(str(qsize[0] * qsize[1]) + '\n')
  for i in range(qsize[0]):
    for j in range(4):
      f1.write(str(i*4 + j + 1))
      #for k in range(3):
      #  f1.write(' ' + str(quads[i, j, k]))
      f1.write(' ' + str((quads[i, j, 0] * 70.66 / xsize) - (70.66 / 2)))
      f1.write(' ' + str((70.66 / 2) - (quads[i, j, 1] * 70.66 / xsize)))
      f1.write(' ' + str((24.73 / 2) - ((quads[i, j, 2] + 1) * 24.73 / zsize)))
      f1.write('\n')
  f1.write("$EndNodes\n")

  f1.write("$Elements\n")
  f1.write(str(qsize[0]) + '\n')
  for i in range(qsize[0]):
    f1.write(str(i + 1))
    f1.write(" 3 2 101 100")
    for j in range(4):
      f1.write(' ' + str(i*4 + j + 1))
    f1.write('\n')
  f1.write("$EndElements\n")

  f1.close()
  return

def get_quad(j, x, y, z):
  quad = np.zeros((4, 3), dtype=np.uint8)
  if j==1:   # right
    quad[0] = (x+1, y  , z  )
    quad[1] = (x+1, y+1, z  )
    quad[2] = (x+1, y+1, z+1)
    quad[3] = (x+1, y  , z+1)
  elif j==2: # left
    quad[0] = (x  , y+1, z  )
    quad[1] = (x  , y  , z  )
    quad[2] = (x  , y  , z+1)
    quad[3] = (x  , y+1, z+1)
  elif j==3: # back
    quad[0] = (x+1, y+1, z  )
    quad[1] = (x  , y+1, z  )
    quad[2] = (x  , y+1, z+1)
    quad[3] = (x+1, y+1, z+1)
  elif j==4: # front
    quad[0] = (x  , y  , z  )
    quad[1] = (x+1, y  , z  )
    quad[2] = (x+1, y  , z+1)
    quad[3] = (x  , y  , z+1)
  elif j==5: # top
    quad[0] = (x  , y  , z+1)
    quad[1] = (x+1, y  , z+1)
    quad[2] = (x+1, y+1, z+1)
    quad[3] = (x  , y+1, z+1)
  elif j==6: # bottom
    quad[0] = (x  , y+1, z  )
    quad[1] = (x+1, y+1, z  )
    quad[2] = (x+1, y  , z  )
    quad[3] = (x  , y  , z  )
  return quad

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

# probe cell adjacency
#  and create list of bounding surface quads
quads = np.zeros((xsize*ysize, 4, 3), dtype=np.uint16) # hopefully this empty list is long enough!!! 
qcnt = 0 # the total number of surface quads
cnts = np.zeros((8, 8), dtype=np.uint16) # adjacency counts matrix
vals = np.zeros((7), dtype=np.uint8)  # temp: voxel neighbor values
cvs = np.unique(images)
print "\ncell voxel counts:"
for cv in cvs[1:]:
  xyz = np.where(images == cv)
  z = xyz[0]
  y = xyz[1]
  x = xyz[2]
  print ' ', cv, x.shape[0]
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
        if vals[j] == 0: # outer boundry?
          quads[qcnt] = get_quad(j, x[i], y[i], z[i])
          qcnt += 1

print "\ncell voxel face adjacency counts:"
print cnts[1:], '\n' # adjacency matrix
#print np.sum(cnts, axis=0)[0], qcnt

write_msh(xsize, ysize, zsize, quads[0:qcnt]) # save the bounding mesh

