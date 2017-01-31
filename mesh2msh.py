#!/usr/bin/python

import numpy as np

# parameters
mdir = "mesh3d/"
fname = "out_p6-p4-p8"

# functions
def unique_rows(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))

# input
print "input mesh data file"
f1 = open(mdir+fname+".mesh", 'r')

for line in f1: 
  if line.startswith("Vertices"): break
nverts = int(f1.next())
verts = np.empty((nverts, 3), dtype=np.float)
for i in range(nverts):
  verts[i] = map(float,f1.next().split()[0:3])

for line in f1: 
  if line.startswith("Triangles"): break
ntris = int(f1.next())
tris = np.empty((ntris,4), dtype=int)
for i in range(ntris): 
  tris[i] = map(int,f1.next().split())

f1.close()
tris = unique_rows(tris) # remove outer face duplicates
ntris = len(tris)
print "  vertices: %d" % nverts
print " triangles: %d" % ntris

# topology
print "identify cell topology"
cells = np.unique(tris[:,3])
for cell in cells: # for each cell
  print("  cell: %d" % cell)
  cell_tris = (tris[tris[:,3] == cell][:,0:3])
  ncell_tris = len(cell_tris)
  print("    triangles: %d" % ncell_tris)
  V = []                            # list of all v indices
  E = np.empty((0,4), dtype=np.int) # indices of v1,v2,f1,f2
  F = np.empty((0,9), dtype=np.int) # indices of v1,v2,v3,e1,e2,e3,f1,f2,f3
  for tri in cell_tris:
    for p in tri[0:3]: V.append(p)
    temp = np.sort([tri[0], tri[1]])
    E = np.append(E, np.array([[temp[0],temp[1],0,0]]), axis=0)
    temp = np.sort([tri[1], tri[2]])
    E = np.append(E, np.array([[temp[0],temp[1],0,0]]), axis=0)
    temp = np.sort([tri[2], tri[0]])
    E = np.append(E, np.array([[temp[0],temp[1],0,0]]), axis=0)
    F = np.append(F, np.array([[tri[0],tri[1],tri[2],0,0,0,0,0,0]]), axis=0)
  V = list(set(V)) # unique V's
  E = unique_rows(E)
  print "      V:%d" % len(V)
  print "      E:%d" % len(E)
  print "      F:%d" % len(F)

# output
print "output msh data file"

f2 = open(mdir+fname+".msh", 'w')
f2.write("$MeshFormat\n")
f2.write("2.2 0 8\n")
f2.write("$EndMeshFormat\n")

f2.write("$Nodes\n")
f2.write("%d\n" % nverts)
for i,p in enumerate(verts):
  f2.write("%d %7.3f %7.3f %7.3f\n" % (i+1, p[0], p[1], p[2]))
f2.write("$EndNodes\n")

f2.write("$Elements\n")
f2.write("%d\n" % (len(tris)))
n = 0
for cell in cells: # for each cell
  for tri in tris[tris[:,3] == cell][:,0:3]: # for each triangle
    n += 1
    f2.write("%d 2 2 0 %d %d %d %d\n" % (n, cell, tri[0], tri[1], tri[2]))
f2.write("$$EndElements\n")
f2.close()

