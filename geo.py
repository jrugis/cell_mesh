#!/usr/bin/python

import numpy as np
from scipy.interpolate import splprep, splev
from operator import add
from pyevtk.hl import pointsToVTK

# indices to coordinates
def i2xyz(ijk, size):
  x = ((ijk[0]) * 70.66 / size[0]) - (70.66 / 2)
  y = (70.66 / 2) - ((ijk[1]) * 70.66 / size[1])
  z = (24.73 / 2) - ((ijk[2]+1) * 24.73 / (size[2]-2))
  return np.array([x,y,z])

# recursively find next point on line
def next_point(slabels, ijk, end_label, line_label, llist):
  llist.append(ijk)
  slabels['hit'][tuple(ijk)] = 1 # mark space point as hit
  adj = [[-1,0,0],[1,0,0],[0,-1,0],[0,1,0],[0,0,-1],[0,0,1]]
  for n in range(len(adj)): # scan adjacent points
    t = map(add, ijk, adj[n])
    if (slabels['hit'][tuple(t)] != 1): # already hit?
      l = slabels['label'][tuple(t)]
      if (l == line_label) or (l == end_label): # on the line?
        next_point(slabels, t, end_label, line_label, llist) # keep going
  return

# save vtk geometry files
def save_vtk(fd, label, pnts, size):
  n = pnts.shape[0]
  print("  label:%-4s count:%i"% (label, n))
  xyz = np.zeros((n,3), dtype=np.float)
  for i, p in enumerate(pnts):
    xyz[i] = i2xyz(p, size)
  np.savetxt(fd+'geom_'+label+".dat", xyz, fmt='%2.4f') # text file
  d = {}                                      # vtk file
  null = np.full(n, 0.0)                      #
  d["null"] = null                            #    
  pointsToVTK(fd+'geom_'+label, xyz[:,0], xyz[:,1], xyz[:,2], d)
  return

# save a gmsh geo line
def save_line(f, pcnt, lcnt, end_label, line_label, size, pnts, slabels):
  llist = []
  for t in np.where(pnts['label']==end_label)[0]: # find the end points
    ijk = pnts['ijk'][t].tolist()  # get end point indices
    slabels['hit'][tuple(ijk)] = 0 # clear end point hits
  next_point(slabels, ijk, end_label, line_label, llist) # walk from the last end point
  ll = len(llist)
  for i in range(ll):
    f.write("Point(" + str(pcnt+i+1) + ") = {%2.4f, %2.4f, %2.4f, lc};\n"% (tuple(i2xyz(llist[i], size))))
  f.write("\n")
  f.write("Line("+str(lcnt+1)+") = {")
  for i in range(ll):
    f.write(str(pcnt+i+1))
    if i < (ll-1): f.write(",")
  f.write("} ;\n")
  f.write("BSpline("+str(lcnt+2)+") = {")
  for i in range(ll):
    f.write(str(pcnt+i+1))
    if i < (ll-1): f.write(",")
  f.write("};\n")
  f.write("\n")
  return ll

# save gmsh geo file
def save_geo(fname, size, pnts, slabels):
  f = open(fname, 'w')
  f.write("//\n")
  f.write("//\n")
  f.write("//\n")
  f.write("\n")
  f.write("lc = 5e-1;\n")
  f.write("\n")
  pcnt = save_line(f, 0, 0, "0567", "067", size, pnts, slabels)
  #pcnt = save_line(f, pcnt, 2, "0567", "567", size, pnts, slabels)
  f.write("Coherence Mesh;\n")
  f.close()
  return

# save a cgal polyline
def save_pline(f, end_label, line_label, size, pnts, slabels):

  llist = [] # get list of line indicies
  for t in np.where(pnts['label']==end_label)[0]: # find the end points
    ijk = pnts['ijk'][t].tolist()  # get end point indices
    slabels['hit'][tuple(ijk)] = 0 # clear end point hits
  next_point(slabels, ijk, end_label, line_label, llist) # walk from the last end point
 
  points = np.zeros((len(llist[0]), len(llist))) # indicies -> point coordinates
  for i in range(len(llist)): 
    #points[:,i] = i2xyz(llist[i], size)
    points[0,i] = 8 * 0.069 * llist[i][0]
    points[1,i] = 8 * 0.069 * llist[i][1]
    points[2,i] = 0.798 * llist[i][2]

  s = 10.0 # smoothness parameter
  k = 3 # b-spline order
  nest = -1 # estimate of number of knots needed (-1 = maximal)
  tckp,u = splprep(points, s=s, k=k, nest=-1) # find b-spline knot points
  xnew,ynew,znew = splev(np.linspace(0, 1, 30), tckp) # interpolate smooth points

  f.write(str(len(xnew))+" ")
  for i in range(len(xnew)):
    f.write("%2.4f %2.4f %2.4f "% (xnew[i], ynew[i], znew[i]))
  f.write('\n')

  ##import mayavi.mlab as mylab
  ##mylab.plot3d(points[0], points[1], points[2], color=(1,0,0))
  ##mylab.plot3d(xnew, ynew, znew, color=(0,1,0))
  ##mylab.show()
  return

# save cgal polylines file
def save_polylines(fname, size, pnts, slabels):
  f = open(fname, 'w')
  save_pline(f, "0567", "067", size, pnts, slabels)
  f.close()
  return

