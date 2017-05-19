#!/usr/bin/python

import sys
import numpy as np

if len(sys.argv) != 2:
    print "Usage: CorrelatedDM.py QCHEM-output"
    exit(0)

fn_qchem = sys.argv[1]

def extract_diagonal(fn_qchem):

    count = 0
    with open(fn_qchem, 'r') as f:
        lines = f.readlines()
        for line in lines:
            if 'MP2 density matrix' in line:
                count += 1
            elif 'm_pdata' in line:
                tokens = line.split()
                if len(tokens) != 5:
                    
        #if 'm_pdata' in line:
            tokens = line.split()

    return count

if __name__ == "__main__":

    count = extract_diagonal(fn_qchem)
    print count
