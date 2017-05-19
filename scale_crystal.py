#!/usr/bin/python

import sys
import numpy as np

if len(sys.argv) != 5:
    print "Usage: scale_crystal.py unscaled_xyz a b c"
    exit(0)

fn_xyz = sys.argv[1]
a = float(sys.argv[2])
b = float(sys.argv[3])
c = float(sys.argv[4])

sym = []
x = []
y = []
z = []
with open(fn_xyz, 'r') as f:
    Natoms = int(f.readline())
    lines = f.readlines()[1:]
    for line in lines:
        tokens = line.split()
        sym.append(tokens[0])
        x.append(float(tokens[1]))
        y.append(float(tokens[2]))
        z.append(float(tokens[3]))

x_new = []
y_new = []
z_new = []
for i in range(Natoms):
     x_new = x[i] * a
     y_new = y[i] * b
     z_new = z[i] * c

     print sym[i],"    ",x_new,"    ",y_new,"    ",z_new
