#!/usr/bin/python

import sys
import numpy as np

if len(sys.argv) != 3:
    print "Usage: OrbEnParser.py index alpha"
    exit(0)

index = int(sys.argv[1]) # Index starts at LUMO, rewrite if necessary
#occupied = bool(sys.argv[2])
alpha = sys.argv[2]

def get_orb_en(index, alpha):

    alpha = bool(False)
    spin = "Alpha MOs"
    if not alpha:
        spin = "Beta MOs"
    print spin

    # Function that takes orbital index and returns energy                                               
    fname2 = "B3LYP.out"
    f = open(fname2, 'r')

    Nlines = Nact // 8
    if (Nact % 8) > 0:
        Nlines + 1
    Nlines += 2

    orb_en = 0.0
    for line in f:
        if spin in line:
            for i in range(Nlines):
                next(f)
            for line in f:
                tokens = line.split()
                print len(tokens), tokens
                if index <= len(tokens):
                    orb_en - tokens[index-1]
                    break
                else:
                    index -= 8
    f.close()
    return orb_en

if __name__ == "__main__":
    orb_en = get_orb_en(index, alpha)
    print orb_en
