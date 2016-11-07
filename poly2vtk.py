#!/usr/bin/python

import numpy as np
from pyevtk.hl import pointsToVTK

pdir = "geometry/"
fname = "polylines"

####################
print "input polyline data file"
f1 = open(pdir+fname+".txt", 'r')

for line in f1: 
  l = line.split()
  pcount = int(l[0])
  xyz = np.empty((pcount, 3), dtype=np.float)
  for t in range(pcount):
    xyz[t] = map(float,line.split()[3*t+1:3*t+4])

f1.close()

####################
print "output polyline data points"
d = {}                                      # vtk file
null = np.full(pcount, 0.0)                 #
d["null"] = null                            #    
pointsToVTK(pdir+fname, xyz[:,0]-35.33, 35.33-xyz[:,1], 11.59-xyz[:,2], d)
#pointsToVTK(pdir+fname, xyz[:,0], xyz[:,1], xyz[:,2], d)

####################

