#!/usr/bin/python

import numpy as np

mdir = "mesh3d/"
fname = "out_p6-p4-p8"

####################
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
trisc = int(f1.next())
tris = np.empty((trisc,4), dtype=int)
for t in range(trisc): 
  tris[t] = map(int,f1.next().split())

for line in f1: 
  if line.startswith("Tetrahedra"): break
tetsc = int(f1.next())
tets = np.empty((tetsc,5), dtype=int)
for t in range(tetsc):
  tets[t] = map(int,f1.next().split())

f1.close()

####################
print "identify geometry"

ftype = [('v0', np.int),('v1', np.int),('v2', np.int),('label', 'S2')]
faces = np.empty(trisc/2, dtype=ftype)
for i in range(len(faces)):
  faces[i] = (tris[2*i][0],tris[2*i][1],tris[2*i][2],str(tris[2*i][3])+str(tris[2*i+1][3]))
fl, lc = np.unique(faces['label'], return_counts=True)

vtype = [('v0', np.int),('v1', np.int),('v2', np.int),('v3', np.int),('label', 'S1')]
vols = np.empty(tetsc, dtype=vtype)
for i in range(tetsc):
  vols[i] = (tets[i][0],tets[i][1],tets[i][2],tets[i][3],str(tets[i][4]))
vl, vc = np.unique(vols['label'], return_counts=True)

####################
print "output vtk data files for faces"

for i, f in enumerate(fl):
  f2 = open(mdir+fname+"_"+fl[i]+".vtk", 'w')
  f2.write("# vtk DataFile Version 2.0\n")
  f2.write("mesh data\n")
  f2.write("ASCII\n")
  f2.write("DATASET UNSTRUCTURED_GRID\n")

  f2.write("POINTS "+str(pcount)+" float\n")
  for v in xyz:
    f2.write(str(v[0]-35.33)+' '+str(35.33-v[1])+' '+str(11.59-v[2])+'\n')

  f2.write("CELLS "+str(lc[i])+" "+str(lc[i]*4)+"\n")
  for v in faces:
    if v[3] == f:
      f2.write("3 "+str(v[0]-1)+' '+str(v[1]-1)+' '+str(v[2]-1)+'\n')

  f2.write("CELL_TYPES "+str(lc[i])+"\n")
  for t in range(lc[i]): f2.write("5 ")
  f2.write("\n")

  f2.close()

####################
print "output vtk data files for volumes"

for i, f in enumerate(vl):
  f2 = open(mdir+fname+"_"+vl[i]+".vtk", 'w')
  f2.write("# vtk DataFile Version 2.0\n")
  f2.write("mesh data\n")
  f2.write("ASCII\n")
  f2.write("DATASET UNSTRUCTURED_GRID\n")

  f2.write("POINTS "+str(pcount)+" float\n")
  for v in xyz:
    f2.write(str(v[0]-35.33)+' '+str(35.33-v[1])+' '+str(11.59-v[2])+'\n')

  f2.write("CELLS "+str(vc[i])+" "+str(vc[i]*5)+"\n")
  for v in vols:
    if v[4] == f:
      f2.write("4 "+str(v[0]-1)+' '+str(v[1]-1)+' '+str(v[2]-1)+' '+str(v[3]-1)+'\n')

  f2.write("CELL_TYPES "+str(vc[i])+"\n")
  for t in range(vc[i]): f2.write("10 ")
  f2.write("\n")

  f2.close()

####################

