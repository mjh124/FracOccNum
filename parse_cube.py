#!/usr/bin/python

import sys
import numpy as np

if len(sys.argv) != 2:
    print "Usage: parse_cube.py cube-file"
    exit(0)

fn_cube = sys.argv[1]

with open(fn_cube, 'r') as f:
    lines = f.readlines()[3:6]

x_points = lines[0].split()[0]
y_points = lines[1].split()[0]
z_points = lines[2].split()[0]

x_space = lines[0].split()[1]
y_space = lines[1].split()[2]
z_space = lines[2].split()[3]


