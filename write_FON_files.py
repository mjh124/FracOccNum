#!/usr/bin/python

import sys
import numpy as np
from subprocess import check_call, check_output

if len(sys.argv) != 3:
    print "Usage: write_FON_files.py a-temp b-temp"
    exit(0)

aTemp = int(sys.argv[1])
bTemp = int(sys.argv[2])

def write_FON(fn, temp):

    with open(fn, 'r') as f_in:
        line = f_in.readline()
        tokens = line.split()
    with open(fn, 'w') as f_out:
        tokens[2] = temp
        for i in range(len(tokens)):
            f_out.write('%d ' % (float(tokens[i])))

if __name__ == "__main__":

    #FON_files = ['FONa.dat', 'FONb.dat']
    #for i in FON_files:
    #    write_FON(i)
    write_FON('FONa.dat', aTemp)
    write_FON('FONb.dat', bTemp)
