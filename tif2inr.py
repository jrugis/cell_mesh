
import libtiff as tf
import numpy as np

fdir = "layers/"
fname = "cellsN"
mdir = "mesh3d/"
mname = "cells.inr"

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

# output inr file
print "output inr file"
header = "#INRIMAGE-4#{\n"
header += "XDIM="+str(xsize)+"\n"
header += "YDIM="+str(ysize)+"\n"
header += "ZDIM="+str(zsize)+"\n"
header += "VDIM=1\n"
header += "TYPE=unsigned fixed\n"
header += "PIXSIZE=8 bits\n"
header += "SCALE=2**0\n"
header += "CPU=pc\n"
header += "VX=0.069\n"
header += "VY=0.069\n"
header += "VZ=0.824\n"
header += "#GEOMETRY=CARTESIAN\n"
for i in range(252-len(header)):
  header += "\n"
header += "##}\n"
f = open(mdir+mname, 'w')
f.write(header)
for d in images:
  f.write(np.int8(d))  
f.close()

