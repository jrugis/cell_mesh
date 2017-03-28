# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt
import numpy as np

fname = 'cell_vol'
fig, ax = plt.subplots()

f = open(fname +'.csv','rb')
d = csv.reader(f)
i = 1
for row in d:
  vals = np.array(row).astype(np.float)
  base = vals[0]
  ax.plot(100*np.divide(vals-base,base), label='cell'+str(i))
  i = i+1
f.close()

legend = ax.legend()

plt.xlabel('smoothing iteration')
plt.ylabel('percent change')
plt.grid()
#plt.show()
plt.savefig(fname+'.pdf')

