# -*- coding: utf-8 -*-
'''
Created on 25.10.17
@author: jrugis
'''

import sys
import math
import numpy as np

tfname = "tubes_20c.msh"

def get_dmin(pnt,arr):
  dmin = sys.float_info.max
  for j in range(arr.shape[0]):
    dxyz = pnt - arr[j]
    d = dxyz[0] * dxyz[0] + dxyz[1] * dxyz[1] + dxyz[2] * dxyz[2]
    if d < dmin: dmin = d
  return math.sqrt(dmin)

# read in tubes coordinates
print tfname,
f = open(tfname)
while f.readline().strip() != '$Nodes': None # skip to the $Nodes section
n = int(f.readline().strip()) # get the number of nodes
print 'tubes node count:', n
tubes = np.zeros((n,3))
for i in range(n):  # get the node coordinate values
  tubes[i] = f.readline().split()[1:4]
f.close()

tdist = np.zeros((n,7))
for p in range(1,8):
  cfname = "out_N4_p3-p2-p4-" + str(p) + "tet.msh"
  print cfname, "-",

  # read in cell coordinates
  f = open(cfname)
  while f.readline().strip() != '$Nodes': None # skip to the $Nodes section
  n = int(f.readline().strip()) # get the number of nodes
  print 'cell', p, 'node count:', n
  cell = np.zeros((n,3))
  for i in range(n):  # get the node coordinate values
    cell[i] = f.readline().split()[1:4]
  f.close()

  # calculate a 'stretched' cell bounding box
  cmin = np.amin(cell,0)
  cmax = np.amax(cell,0)
  d = (cmax - cmin) / 10  # stretch factor
  cmin -= d
  cmax += d

  for j in range(tubes.shape[0]):
    tdist[j,p-1] = 100.0 
    if (tubes[j,0] >= cmin[0]) and (tubes[j,0] <= cmax[0]):
      if (tubes[j,1] >= cmin[1]) and (tubes[j,1] <= cmax[1]):
        if (tubes[j,2] >= cmin[2]) and (tubes[j,2] <= cmax[2]):
          tdist[j,p-1] = get_dmin(tubes[j], cell)
    if (j % 100) == 0: 
      print j,
      sys.stdout.flush()
  print

# write out the nearest cell number for each tube node 
f = open(tfname, 'a')
f.write('$NodeData\n')
f.write('1\n')                       # one string tag
f.write('"nearest cell number"\n')   #   name
f.write('1\n')                       # one real tag
f.write('0.0\n')                     #   time value
f.write('3\n')                       # three integer tags
f.write('0\n')                       #   time step
f.write('1\n')                       #   one component (scalar)
f.write('%s\n' % str(tubes.shape[0])) #   node count
for i in range(tdist.shape[0]):
  if (min(tdist[i]) >= 0.5):
    cnum = 0
  else:
    cnum = np.argmin(tdist[i]) + 1
  f.write('%d %f\n' % (i+1, cnum))  # node, value
f.write('$EndNodeData\n')
f.close()



