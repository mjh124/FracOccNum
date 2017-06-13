#!/usr/bin/env python

from __future__ import print_function
import numpy as np

# 1. How to open intefral files?

dim = 7 #Hard code in the dimension of the matrix
filename_overlap = "h2o_sto3g_s.dat"

def parse_int_file_2(filename, dim):
    mat = np.zeros(shape=(dim, dim))
    with open(filename) as fh:
        contents = fh.readlines()
    for line in contents:
        sline = line.split()
        mu, nu, intval = map(float, sline) # automatic unpacking alternative in python
        mat[mu-1, nu-1] = mat[nu-1, mu-1] = float(intval)
    return mat

mat = parse_int_file_2(filename_overlap, dim)
print(mat)
