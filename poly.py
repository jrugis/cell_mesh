#!/usr/bin/python

import numpy as np
import scipy.interpolate as si
import mayavi.mlab as mylab

def calc_points(line):
  points = np.zeros((len(line),3)) # indicies -> point coordinates
  for i in range(points.shape[0]): 
    #points[i,0] = 2 * 0.556 * (line[i][0]-0.5)
    #points[i,1] = 2 * 0.556 * (line[i][1]-0.5)
    #points[i,2] = 0.798 * (line[i][2]-0.5) # z axis
    points[i,0] = 0.556 * (line[i][0]-0.5)
    points[i,1] = 0.556 * (line[i][1]-0.5)
    points[i,2] = 0.798 * (line[i][2]-0.5) # z axis
    #points[i,0] = 0.556 * (line[i][0])
    #points[i,1] = 0.556 * (line[i][1])
    #points[i,2] = 0.798 * (line[i][2]) # z axis
  return points

def bspline(cv, n=100, degree=3):
  cv = np.asarray(cv)
  count = cv.shape[0]
  degree = np.clip(degree,1,count-1) # max degree = count-1
  kv = np.array([0]*degree + range(count-degree+1) + [count-degree]*degree,dtype='int')
  u = np.linspace(0,(count-degree),num=n)
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
    #spoints = bspline(points, n=points.shape[0], degree=20)
    m = len(points)/2
    if m<4: continue
    kx = 3
    #if(m>3): kx = 3
    #else: kx = m-1
    wx = np.ones(len(points))
    wx[0] = wx[-1] = 100
    tck,u=si.splprep(np.transpose(points),w=wx,k=kx,s=10)
    #m /= 2
    #if(m<4) : m=4
    spoints = np.transpose([si.splev(np.linspace(0,1,m),tck)])
    f.write("%2d " % m) 
    for spoint in spoints:
      for vert in spoint:
        f.write("%0.2f " % vert)
    f.write('\n')
    mylab.plot3d(points[:,0], points[:,1], points[:,2], color=(1,0,0))   
    mylab.plot3d(spoints[:,0], spoints[:,1], spoints[:,2], color=(0,1,0))
  f.close()
  mylab.show()
  return

