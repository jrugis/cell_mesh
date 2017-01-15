#!/usr/bin/python

import numpy as np
from operator import add

#########################################################################################

# line segment scan offset parameter array: 
#    [segment base offset, segment XYZ direction, offset to next segment base]
SEG_PARMS = [[[0,0,0],0,[1,0,0]],[[0,0,0],1,[0,1,0]],[[0,0,0],2,[0,0,1]],
             [[-1,0,0],0,[-1,0,0]],[[0,-1,0],1,[0,-1,0]],[[0,0,-1],2,[0,0,-1]]]

# check line segment coverage
def check_lsegs(slabels):
  ls = 0
  for k in range(slabels.shape[2]):
    for j in range(slabels.shape[1]):
      for i in range(slabels.shape[0]):
        for n in range(3):
          if slabels['xyzlabel'][i,j,k][n] != "" :
            if slabels['xyzhit'][i,j,k][n] != True :
              print [i,j,k], n, "NOT HIT"
            ls += 1
  return ls

# identify and label all line segments
def line_segs(voxels, slabels): 
  adj = [[0,-1,-1],[-1,0,-1],[-1,-1,0]] # voxel kernel direction offsets
  segs = 0
  for k in range(1, slabels.shape[2]):
    for j in range(1, slabels.shape[1]):
      for i in range(1, slabels.shape[0]):
        for n in range(len(adj)): # check xyz directions
          p4 = voxels[i+adj[n][0]:i+1, j+adj[n][1]:j+1, k+adj[n][2]:k+1]
          vals = np.unique(p4) # what cells are in this 4 voxel kernel?
          if len(vals) > 2: 
            segs += 1
            slabels['xyzlabel'][i,j,k][n] = ''.join(map(str,vals))
  return segs

#########################################################################################

# how many line segments meet at this point?
def line_count(i, j, k, slabels): 
  lcnt = 0
  for a in SEG_PARMS: # six directions
    if slabels['xyzlabel'][tuple(map(add, [i,j,k], a[0]))][a[1]] != "":
      lcnt += 1
  return lcnt

# cull singleton line segments
def line_cull(slabels): 
  culled = 0
  for k in range(1, slabels.shape[2]):
    for j in range(1, slabels.shape[1]):
      for i in range(1, slabels.shape[0]):
        if line_count(i,j,k, slabels) == 1: # single segment at this point?
          culled += 1
          for a in SEG_PARMS:
            slabels['xyzlabel'][tuple(map(add, [i,j,k], a[0]))][a[1]] = ""
  return culled

# identify end points
def end_points(slabels):
  endp = 0
  for k in range(1, slabels.shape[2]):
    for j in range(1, slabels.shape[1]):
      for i in range(1, slabels.shape[0]):
        if line_count(i,j,k, slabels) > 2: # more than two lines meet here?  
          endp += 1
          slabels['endp'][i,j,k] = True
  return endp

#########################################################################################

# add point to line (recursive)
def next_point(first, slabels, p, adj, lpnts):
  if not first and slabels['endp'][tuple(p)]:
      return # end point?
  slabels['xyzhit'][tuple(map(add, p, adj[0]))][adj[1]] = True # mark segment as hit
  p = map(add, p, adj[2]) # the next point
  lpnts.append(p) # add next point to list
  for a in SEG_PARMS: # six directions
    if ((slabels['xyzlabel'][tuple(map(add, p, a[0]))][a[1]] != "")
    and (slabels['xyzhit'][tuple(map(add, p, a[0]))][a[1]] == False)):
      next_point(False, slabels, p, a, lpnts) # found another segment
      break
  return # done

# scan around an end point for segments not hit
def scan_endp(p, lpnts, slabels):
  for a in SEG_PARMS: # six directions
    if ((slabels['xyzlabel'][tuple(map(add, p, a[0]))][a[1]] != "")
    and (slabels['xyzhit'][tuple(map(add, p, a[0]))][a[1]] == False)):
      lpnts.append([p]) # create a new line list with first point
      next_point(True, slabels, p, a, lpnts[-1])
  return

# get geometry lines
def get_lines(slabels):
  endp = np.transpose(np.vstack(np.where(slabels['endp']==True))).tolist()
  lpnts = [] # list of point lists
  for p in endp:
    scan_endp(p, lpnts, slabels)
  return lpnts

#########################################################################################


