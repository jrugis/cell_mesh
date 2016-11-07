#!/usr/bin/python

### NOT USED

import numpy as np
import os
from scipy.interpolate import splprep, splev
import struct

fdir = "mesh3d/"
fname = "cells.inr"

f1 = open(fdir+fname, 'r')
for line in f1:
  if line.startswith("XDIM"): break
xdim = int(line.split('=')[1])
ydim = int(f1.next().split('=')[1])
zdim = int(f1.next().split('=')[1])
print xdim, ydim, zdim

for line in f1:
  if line.startswith("VX"): break
vx = float(line.split('=')[1])
vy = float(f1.next().split('=')[1])
vz = float(f1.next().split('=')[1]) 
print vx, vy, vz

f1 = open(fdir+fname, 'rb')
f1.seek(256, os.SEEK_SET) # skip to binary data

xyz = np.fromfile(f1, dtype=np.int8)
xyz = np.reshape(xyz, (xdim,ydim,zdim))
print np.shape(xyz)

f1.close()

#for k in range(zdim):
#  for j in range(ydim):
#   for i in range(xdim):
#      xyz[i,j,k] = 1


f1.close()

