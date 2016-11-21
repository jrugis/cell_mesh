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

