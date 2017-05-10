# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt
import numpy as np

for i in range(1,8):
  fig,ax = plt.subplots()
  ax.set_xlim([-0.5,0.5])
  ax.set_ylim([0,25])
  bins = np.linspace(-0.5,0.5,99)

  f = open('cell'+str(i)+'_curv0.csv','rb')
  d = csv.reader(f)
  vals = []
  for val in d:
    vals.append(np.float(val[0]))
  f.close()
  vals = np.asarray(vals)
  plt.hist(vals,bins,normed=True,color='#a07040',alpha=0.7,label='initial')

  f = open('cell'+str(i)+'_curv10.csv','rb')
  d = csv.reader(f)
  vals = []
  for val in d:
    vals.append(np.float(val[0]))
  f.close()
  vals = np.asarray(vals)
  plt.hist(vals,bins,normed=True,color='#0080ff',alpha=0.7,label='final')

  plt.rcParams.update({'font.size': 16})
  ax.legend(loc=1,prop={'size':14})
  plt.title('Cell'+str(i)+': surface curvature change')
  plt.xlabel('curvature')
  plt.ylabel('normalised counts')

  #plt.show()
  plt.savefig('cell'+str(i)+'_curv_morph.pdf')

