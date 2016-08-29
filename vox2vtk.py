#!/bin/bash

import numpy as np
import libtiff as tf
from pyevtk.hl import pointsToVTK

fdir = "layers/"
fname = "cellsNR"

f1 = tf.TIFF3D.open(fdir+fname+".tif", mode='r') 
images = f1.read_image()    # load the image stack
f1.close()
print images.shape

icount = images.shape[0]    # image count in stack
isize = images.shape[1]     # side dimension of images


cvs = np.unique(images)
for cv in cvs[1:]:
  print cv
  xyz = np.where(images == cv)
  #z = -(xyz[0] * 105.0 / isize) + 10.5
  z = (24.73 / 2) - ((xyz[0] + 1) * 24.73 / icount)
  x = (xyz[2] * 70.66 / isize) - (70.66 / 2)
  y = (70.66 / 2) - (xyz[1] * 70.66 / isize)
  null = np.full(x.shape, cv)
  d = {}
  d["null"] = null
  pointsToVTK(fdir+fname+str(cv), x, y, z, d) # write out vtk file

