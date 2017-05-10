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

  fig,ax = plt.subplots()
  ax.set_xlim([-0.5,0.5])
  ax.set_ylim([0,14])
  bins = np.linspace(-0.5,0.5,99)
  plt.hist(vals,bins,normed=True,color='#0080ff',alpha=0.7)
  plt.rcParams.update({'font.size': 16})
  plt.title('Cell'+str(i)+': image slice curvature distribution')
  plt.xlabel('curvature')
  plt.ylabel('normalised counts')

  #plt.show()
  plt.savefig('cell'+str(i)+'_curv.pdf')

