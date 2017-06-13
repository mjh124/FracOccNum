#!/usr/bin/python

import sys
import numpy as np
from subprocess import check_call, check_output

if len(sys.argv) != 2:
    print "Usage: write_FON_files.py temperature"
    exit(0)

temp = int(sys.argv[1])

def write_FON(fn):

    with open(fn, 'r') as f_in:
        line = f_in.readline()
        tokens = line.split()
    with open(fn, 'w') as f_out:
        tokens[2] = temp
        for i in range(len(tokens)):
            f_out.write('%d ' % (float(tokens[i])))

if __name__ == "__main__":

    FON_files = ['FONa.dat', 'FONb.dat']
    for i in FON_files:
        write_FON(i)
