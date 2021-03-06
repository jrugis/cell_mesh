#!/usr/bin/python

import numpy as np
import scipy.misc as sm
import libtiff as tf
#import matplotlib.pyplot as plt
#import sys

#def show_image(img):
#  f1 = plt.figure()
#  f1 = plt.imshow(img, interpolation='nearest', cmap="gray")
#  plt.colorbar()
#  plt.draw()
#  f2 = plt.figure()
#  f2 = plt.hist(img.ravel(), bins=256)
#  plt.draw()

fdir = "layers/"
fname = "cellsN"

f1 = tf.TIFF3D.open(fdir+fname+".tif", mode='r') 
images = f1.read_image()    # load the image stack
f1.close()
print images.shape
#show_image(images[19])

icount = images.shape[0]    # image count in stack
isize = images.shape[1]     # side dimension of images
bsize = 32                 # decimation block size, MUST DIVIDE isize !!!
bcount = isize / bsize      # side dimension of reduced images
imagesR = np.zeros((icount, bcount, bcount), dtype=np.uint8) # reduced images array
print imagesR.shape

for c in range(icount):     # reduce each image
  imagesR[c] = sm.imresize(images[c], (bcount, bcount), interp='nearest')

#  print c+1
#  print np.unique(images[c])
#  print np.unique(imagesR[c])
print np.unique(images)
print np.unique(imagesR)

f2 = tf.TIFF3D.open(fdir+fname+str(bsize)+"R.tif", mode='w')
f2.write_image(imagesR)     # save the reduced image stack
f2.close()

#imagesD = np.zeros((isize, isize), dtype=np.uint8) # errors array
#for i in range(isize):
#  for j in range(isize):
#    if (images[9,i,j] == 162):
#      imagesD[i,j] == 0
#      print i,j

#imagesD = np.zeros((icount, isize, isize), dtype=np.uint8) # errors array
#for c in range(icount):     # check each image
#  print c,
#  sys.stdout.flush()
#  for i in range(isize):
#    for j in range(isize):
#      if images[c,i,j] in [0, 139, 162, 175, 201, 208, 222, 234]:
#        imagesD[c,i,j] = 255
#      else:
#        imagesD[c,i,j] = 0
#f3 = tf.TIFF3D.open(fdir+fname+"D.tif", mode='w')
#f3.write_image(imagesD)     # errors labelled
#f3.close()

#show_image(imagesR[19])
#plt.show()

##
## Resample by maximum vote. An alternative to nearest neighbor.
##   Note: Much slower.
##
#  for bi in range(bcount):
#    for bj in range(bcount):
#      counts = {}
#      for i in range(bsize):
#        for j in range(bsize):
#          pval = str(images[c, bi*bsize+i, bj*bsize+j])
#          if pval in counts:
#            counts[pval] += 1
#          else:
#            counts[pval] = 1
#      imagesR[c, bi, bj] = np.uint8(max(counts, key=counts.get))

