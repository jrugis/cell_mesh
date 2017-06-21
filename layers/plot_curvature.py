# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt
import numpy as np

for i in range(1,8):
  f = open('cell'+str(i)+'_curv.csv','rb')
  d = csv.reader(f)
  vals = []
  for val in d:
    vals.append(np.float(val[0]))
  f.close()
  vals = np.asarray(vals)

  f = open('cell'+str(i)+'_wght.csv','rb')
  d = csv.reader(f)
  wghts = []
  for val in d:
    wghts.append(np.float(val[0]))
  f.close()
  wghts = np.asarray(wghts)

  fig,ax = plt.subplots()
  ax.set_xlim([-2.0,2.0])
  ax.set_ylim([0.0,3.5])
  plt.hist(vals,bins=80,range=(-2.0,2.0),normed=True,weights=wghts,color='#0080ff',alpha=0.7)
  plt.rcParams.update({'font.size': 16})
  plt.title('Cell'+str(i)+': image slice curvature distribution')
  plt.xlabel('curvature')
  plt.ylabel('normalised counts')

  #plt.show()
  plt.savefig('cell'+str(i)+'_curv.pdf')

