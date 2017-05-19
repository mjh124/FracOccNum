#!/usr/bin/python

import sys
import numpy as np

if len(sys.argv) != 4:
    print "Usage: ON2Idx_test.py ON_string Nocc Nvirt"
    exit(0)

ON_string = str(sys.argv[1])
Nocc = int(sys.argv[2])
Nvirt = int(sys.argv[3])

def get_single_index(ON_string, Nocc, Nvirt):

    ON = list(ON_string)
    occ = ON[:Nocc]
    virt = ON[Nocc:]
    print occ, virt

    occ_idx = []
    for i in range(len(occ)):
        if float(occ[i]) == 0:
            occ_idx.append(i)
    virt_idx = []
    for i in range(len(virt)):
        if float(virt[i]) == 1:
            virt_idx.append(i)

    print occ_idx, virt_idx

    if len(occ_idx) == 1:
        index = occ_idx[0]*Nvirt+virt_idx[0]
    elif len(occ_idx) == 2:
        index = occ_idx[0]*Nocc*Nvirt*Nvirt + occ_idx[1]*Nvirt*Nvirt + virt_idx[0]*Nvirt + virt_idx[1]
    else:
        exit("ERROR: Excitation Level Not Implemented")

    return index

if __name__ == "__main__":

    index = get_single_index(ON_string, Nocc, Nvirt)
    print index
