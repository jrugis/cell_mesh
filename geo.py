#!/usr/bin/python

import numpy as np
import mayavi.mlab as mylab

# temp vis for debug
def view_lsegs(slabels):
  for k in range(slabels.shape[2]):
    for j in range(slabels.shape[1]):
      for i in range(slabels.shape[0]):
        if slabels[i][j][k]['xyzlabel'][0] != "" :
          mylab.plot3d([i,i+1], [j,j], [k,k], color=(1,0,0))
        if slabels[i][j][k]['xyzlabel'][1] != "" :
          mylab.plot3d([i,i], [j,j+1], [k,k], color=(1,0,0))
        if slabels[i][j][k]['xyzlabel'][2] != "" :
          mylab.plot3d([i,i], [j,j], [k,k+1], color=(1,0,0))
  endp = np.where(slabels['endp']==True)
  mylab.points3d(endp[0], endp[1], endp[2], color=(1,1,0), scale_factor=0.75)
  #mylab.plot3d(points[0], points[1], points[2], color=(1,0,0))
  #mylab.plot3d(xnew, ynew, znew, color=(0,1,0))
  mylab.show()
  return

# indices to coordinates
def i2xyz(ijk, size):
  x = ((ijk[0]) * 70.66 / size[0]) - (70.66 / 2)
  y = (70.66 / 2) - ((ijk[1]) * 70.66 / size[1])
  z = (24.73 / 2) - ((ijk[2]+1) * 24.73 / (size[2]-2))
  return np.array([x,y,z])

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

# how many line segments meet at this point?
def line_count(i, j, k, slabels): 
  lcnt = 0
  if slabels[i][j][k]['xyzlabel'][0] != "": lcnt += 1
  if slabels[i][j][k]['xyzlabel'][1] != "": lcnt += 1
  if slabels[i][j][k]['xyzlabel'][2] != "": lcnt += 1
  if slabels[i-1][j][k]['xyzlabel'][0] != "": lcnt += 1
  if slabels[i][j-1][k]['xyzlabel'][1] != "": lcnt += 1
  if slabels[i][j][k-1]['xyzlabel'][2] != "": lcnt += 1
  return lcnt

# cull singleton line segments
def line_cull(slabels): 
  culled = 0
  for k in range(1, slabels.shape[2]):
    for j in range(1, slabels.shape[1]):
      for i in range(1, slabels.shape[0]):
        if line_count(i,j,k, slabels) == 1:
          culled += 1
          slabels[i][j][k]['xyzlabel'] = ('','','')
          slabels[i-1][j][k]['xyzlabel'][0] = ''
          slabels[i][j-1][k]['xyzlabel'][1] = ''
          slabels[i][j][k-1]['xyzlabel'][2] = ''
  return culled

# identify end points
def end_points(slabels):
  endp = 0
  for k in range(1, slabels.shape[2]):
    for j in range(1, slabels.shape[1]):
      for i in range(1, slabels.shape[0]):
        if line_count(i,j,k, slabels) > 2:
          endp += 1
          slabels[i][j][k]['endp'] = True
  return endp

# scan around an end point for lines not hit
def scan_endp(lpnts, slabels):
  i = lpnts[0][0]
  j = lpnts[0][1]
  k = lpnts[0][2]
  lcnt = 0
  if (  (slabels[i][j][k]['xyzlabel'][0] != "")
    and (slabels[i][j][k]['xyzhit'][0] == False)): lcnt += 1
  if (  (slabels[i][j][k]['xyzlabel'][1] != "")
    and (slabels[i][j][k]['xyzhit'][1] == False)): lcnt += 1
  if (  (slabels[i][j][k]['xyzlabel'][2] != "")
    and (slabels[i][j][k]['xyzhit'][2] == False)): lcnt += 1
  if (  (slabels[i-1][j][k]['xyzlabel'][0] != "")
    and (slabels[i-1][j][k]['xyzhit'][0] == False)): lcnt += 1
  if (  (slabels[i][j-1][k]['xyzlabel'][1] != "")
    and (slabels[i][j-1][k]['xyzhit'][1] == False)): lcnt += 1
  if (  (slabels[i][j][k-1]['xyzlabel'][2] != "")
    and (slabels[i][j][k-1]['xyzhit'][2] == False)): lcnt += 1
  print lcnt
  #lpnts = np.append(pnts, [[0, 0, 0]], axis=0)
  lpnts = [[]]
  return lpnts

# save cgal polylines file
def save_polylines(fname, slabels):
  f = open(fname+"_poly.txt", 'w')
  endp = np.transpose(np.vstack(np.where(slabels['endp']==True)))
  for p in endp:
    lpnts = scan_endp(np.array([p]), slabels)
    print lpnts
  f.close()
  return

