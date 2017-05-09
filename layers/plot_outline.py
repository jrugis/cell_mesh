# -*- coding: utf-8 -*-

import csv
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
import numpy as np

outlines = [['cell_boundary_5','s','g','pixels'],
            ['cell_boundary_smooth5','+','r','points']]

plt.rcParams.update({'font.size': 12})
fig, ax = plt.subplots()
plt.title('Segmentation Outline')
axins = zoomed_inset_axes(ax,3,loc=4)
axins.set_xlim(510,520)
axins.set_ylim(-180,-170)

for o in outlines:
  f = open(o[0] +'.csv','rb')
  d = csv.reader(f)
  xy = []
  for row in d:
    xy.append(np.array(row).astype(np.float))
  f.close()
  xy = np.transpose(np.asarray(xy))
  axins.scatter(xy[1,:],-xy[0,:],marker=o[1],color=o[2])
  ax.scatter(xy[1,:],-xy[0,:],marker=o[1],color=o[2],label=o[3])

mark_inset(ax,axins,loc1=1,loc2=3,fc="none",ec="0.5")

legend = ax.legend(loc=1,prop={'size':12})
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_aspect('equal')
axins.get_xaxis().set_visible(False)
axins.get_yaxis().set_visible(False)

#plt.show()
plt.savefig('outline.pdf')

