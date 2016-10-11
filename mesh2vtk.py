#!/usr/bin/python

import numpy as np

mdir = "mesh3d/"
fname = "out_p6-p4-p8"

print "input mesh data file"
f1 = open(mdir+fname+".mesh", 'r')

for line in f1: 
  if line.startswith("Vertices"): break
pcount = int(f1.next())
xyz = np.empty((pcount, 3), dtype=np.float)
for t in range(pcount):
  xyz[t] = map(float,f1.next().split()[0:3])

for line in f1: 
  if line.startswith("Triangles"): break
tcount = int(f1.next())
tris = np.empty((tcount, 4), dtype=np.int)
for t in range(tcount):
  tris[t] = map(int,f1.next().split())

f1.close()

print "output vtk data files"
f2 = open(mdir+fname+".vtk", 'w')
f2.write("# vtk DataFile Version 2.0\n")
f2.write("mesh data\n")
f2.write("ASCII\n")
f2.write("DATASET UNSTRUCTURED_GRID\n")

f2.write("POINTS "+str(pcount)+" float\n")
for v in xyz:
  f2.write(str(v[0]-35.33)+' '+str(35.33-v[1])+' '+str(11.59-v[2])+'\n')

f2.write("CELLS "+str(tcount)+" "+str(tcount*4)+"\n")
for v in tris:
  f2.write("3 "+str(v[0]-1)+' '+str(v[1]-1)+' '+str(v[2]-1)+'\n')

f2.write("CELL_TYPES "+str(tcount)+"\n")
for t in range(tcount):
  f2.write("5 ")
f2.write("\n")

f2.close()


print

