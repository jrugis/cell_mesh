#!/usr/bin/python

import numpy as np
from pyevtk.hl import pointsToVTK

pdir = "geometry/"
#fname = "polylines"
fname = "cellsN8R_poly"

def write_vtk(vname, xyz):
  print "output polyline data points: " + vname
  d = {}                                      # vtk file
  null = np.full(pcount, 0.0)                 #
  d["null"] = null                            #    
  pointsToVTK(vname, xyz[:,0]-35.33, 35.33-xyz[:,1], 12.36-xyz[:,2], d)
  #pointsToVTK(fname, xyz[:,0], xyz[:,1], xyz[:,2], d)
  return

print "input polyline data file"
f1 = open(pdir+fname+".txt", 'r')
ln = 0
for line in f1: 
  ln += 1
  l = line.split()
  pcount = int(l[0])
  xyz = np.empty((pcount, 3), dtype=np.float)
  for t in range(pcount):
    xyz[t] = map(float,line.split()[3*t+1:3*t+4])
  write_vtk(pdir+fname+'-'+str(ln), xyz)
f1.close()

