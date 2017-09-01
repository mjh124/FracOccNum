#!/usr/bin/python

import sys
import numpy as np

if len(sys.argv) != 3:
    print "Usage: quick_density_sum.py fn-cube Natoms"
    exit(0)

fn_cube = sys.argv[1]
Natoms = int(sys.argv[2])

def parse_cube(fn_cube, Natoms):

    density = []
    with open(fn_cube, 'r') as f:
        lines = f.readlines()[Natoms+6:]
        for line in lines:
            density.append(float(line.split()[0]))
    return density

if __name__ == "__main__":

    density = parse_cube(fn_cube, Natoms)

    pos = 0.0
    neg = 0.0
    for i in density:
        if i > 0.0:
            pos += i
        else:
            neg += i

    print neg, pos
