#!/usr/bin/python

import numpy as np
import scipy.interpolate as si
import mayavi.mlab as mylab

def calc_points(line):
  points = np.zeros((len(line),3)) # indicies -> point coordinates
  for i in range(points.shape[0]): 
    points[i,0] = 8 * 0.069 * line[i][0] + 0.5
    points[i,1] = 8 * 0.069 * line[i][1] + 0.5
    points[i,2] = 0.798 * line[i][2] + 0.5
  return points

def bspline(cv, n=100, degree=3):
  cv = np.asarray(cv)
  count = cv.shape[0]
  degree = np.clip(degree,1,count-1) # max degree = count-1
  kv = np.array([0]*degree + range(count-degree+1) + [count-degree]*degree,dtype='int')
  u = np.linspace(0,(count-degree),n)
  points = np.zeros((len(u),cv.shape[1]))
  for i in xrange(cv.shape[1]):
    points[:,i] = si.splev(u, (kv,cv[:,i],degree))
  return points

# save geometry lines
def save_poly(fname, lines):
  fname += "_poly.txt"
  f = open(fname, 'w')
  print ' ', fname
  for line in lines:
    points = calc_points(line)
    spoints = bspline(points, n=points.shape[0], degree=20)
    mylab.plot3d(points[:,0], points[:,1], points[:,2], color=(1,0,0))   
    mylab.plot3d(spoints[:,0], spoints[:,1], spoints[:,2], color=(0,1,0))
  f.close()
  mylab.show()
  return

