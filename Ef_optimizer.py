#!/usr/bin/python

import sys
import numpy as np
import random

if len(sys.argv) != 3:
    print "Usage: Ef_optimizer.py num-electrons MO-file"
    exit(0)

Nelec = int(sys.argv[1])
fMO = sys.argv[2]

def read_MO_file(fMO):

    f = open(fMO, 'r')
    MO_en = []
    for line in f:
        MO_en.append(float(line.split()[1]))
    return MO_en

def fd_2_err(MO_en, ef, T):

    k = 3.1668114e-6 #[Ha/K]
    fi = []
    for i in range(len(MO_en)):
        tmp = np.exp((MO_en[i] - ef)/(k*T))
        fd = 1/(1+tmp)
        fi.append(fd)
    calc_elec = np.sum(fi)
    err = (calc_elec - Nelec)**2

    return err

if __name__ == "__main__":

    # Read orbital energy levels
    MO_en = read_MO_file(fMO)

    # Initialize fermi level guesses
    ef_left = min(MO_en)
    ef_right = max(MO_en)
    ef_mid = (ef_left + ef_right)/2
    efs = [ef_left, ef_right, ef_mid]
    print efs

    thres = 1e3
    for _ in range(100):
        error = [0.0 for i in range(len(efs))]
        for i in range(len(efs)):
            err = fd_2_err(MO_en, efs[i], 100000)
            error[i] = err
        print error

        left_diff = abs(error[0] - error[2])
        right_diff = abs(error[1] - error[2])
        print "l = ", left_diff
        print "r = ", right_diff

        # Use left half
        if left_diff < right_diff:
            efs[1] = efs[2]
            efs[2] = (efs[0] + efs[2])/2

        # Use right half
        elif left_diff > right_diff:
            efs[0] = efs[2]
            efs[2] = (efs[1] + efs[2])/2

        # If stuck, move the center position a random distance
#        elif left_diff == right_diff:
#            r = random.uniform(0.25, 0.75)
#            efs[2] = (r*efs[0] + (1-r)*efs[1])

        print " ", efs
