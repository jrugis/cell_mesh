# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt
import numpy as np

#fname = 'cell_vol'
#fname = 'cell_surf'
#fname = '100_iterations/cell_vol_100'
fname = '100_iterations/cell_surf_100'

plt.rcParams.update({'font.size': 16})
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

legend = ax.legend(loc=9,prop={'size':14})

#plt.title('Cells: volume')
plt.title('Cells: surface area')

plt.xlabel('smoothing iteration')
plt.ylabel('percent change')
plt.grid()
#plt.show()
plt.savefig(fname+'.pdf')

