# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt
import numpy as np

fname = 'cell_curv_std'

plt.rcParams.update({'font.size': 16})
fig, ax = plt.subplots()

ref = [0.0412,
       0.0538,
       0.0432,
       0.0491,
       0.0555,
       0.0602,
       0.0544]

f = open(fname +'.csv','rb')
d = csv.reader(f)
i = 0
for row in d:
  vals = np.array(row).astype(np.float)
  ax.plot(np.divide(vals,ref[i]), label='cell'+str(i+1))
  i = i+1
f.close()

legend = ax.legend(loc=9,prop={'size':14})

plt.title('Cells: curvature standard deviation ratio')

plt.xlabel('smoothing iteration')
plt.ylabel('surface curvature / target curvature')
plt.xticks(np.arange(1,11,1))
plt.grid()
#plt.show()
plt.savefig(fname+'.pdf')

