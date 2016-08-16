#!/bin/bash

convert layers/cells_*.tif -colorspace GRAY layers/cells.tif
identify layers/cells.tif
convert layers/cells.tif -negate layers/cellsN.tif


