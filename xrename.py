#!/bin/bash
import os
import subprocess

fdir = "layers/"

for dirpath, dnames, fnames in os.walk(fdir):
  for f in fnames:
    v = f.split('.')[0].split('_')
    new_fname = v[0] + "_" + v[2][0:2] + ".tif"
    subprocess.call("mv " + fdir + f + " " + fdir + new_fname, shell=True)

