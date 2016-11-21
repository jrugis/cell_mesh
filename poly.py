#!/usr/bin/python

import numpy as np

# indices to coordinates
def i2xyz(ijk, size):
  x = ((ijk[0]) * 70.66 / size[0]) - (70.66 / 2)
  y = (70.66 / 2) - ((ijk[1]) * 70.66 / size[1])
  z = (24.73 / 2) - ((ijk[2]+1) * 24.73 / (size[2]-2))
  return np.array([x,y,z])

# get geometry lines
def save_poly(fname, lines):
  fname += "_poly.txt"
  f = open(fname, 'w')
  print ' ', fname
  f.close()
  return

