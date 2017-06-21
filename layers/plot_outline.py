# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import numpy as np

outlines = [['cell_boundary_17','s','g','pixels'],
            ['cell_boundary_smooth17','+','r','points']]

plt.rcParams.update({'font.size': 16})
fig, ax = plt.subplots()
axins = zoomed_inset_axes(ax,4,loc=10)
axins.set_xlim(40,41.3)
axins.set_ylim(-22.3,-23.6)

for o in outlines:
  f = open(o[0] +'.csv','rb')
  d = csv.reader(f)
  xy = []
  for row in d:
    xy.append(np.array(row).astype(np.float))
  f.close()
  xy = np.transpose(np.asarray(xy))
  ax.scatter(xy[1,:],-xy[0,:],marker=o[1],color=o[2],label=o[3])
  axins.scatter(xy[1,:],-xy[0,:],marker=o[1],color=o[2])

mark_inset(ax,axins,loc1=4,loc2=2,fc="none",ec="0.5")

ax.set_title('Segmentation Outline')
legend = ax.legend(loc=2,prop={'size':12})
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_aspect('equal')
axins.get_xaxis().set_visible(False)
axins.get_yaxis().set_visible(False)

#plt.show()
plt.savefig('outline.pdf')

