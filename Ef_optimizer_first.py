#!/usr/bin/python

import sys
import numpy as np
import random

if len(sys.argv) != 4:
    print "Usage: Ef_optimizer.py MO-file num-electrons temperature"
    exit(0)

fMO = sys.argv[1]
Nelec = int(sys.argv[2])
T = int(sys.argv[3])

def read_MO_file(fMO):

    f = open(fMO, 'r')
    MO_en = []
    for line in f:
        MO_en.append(float(line.split()[1]))
    return MO_en

def fermi_dirac(MO_en, ef, T):

    k = 3.1668114e-6 #[Ha/K]
    fi = []
    for i in range(len(MO_en)):
        tmp = np.exp((MO_en[i] - ef)/(k*T))
        fd = 1/(1+tmp)
        fi.append(fd)
    return fi

def fd_2_err(MO_en, ef, T):

    k = 3.1668114e-6 #[Ha/K]
    calc_elec = 0.0
    for i in range(len(MO_en)):
        tmp = np.exp((MO_en[i] - ef)/(k*T))
        fd = 1/(1+tmp)
        calc_elec += fd
    err = (calc_elec - Nelec)**2

    return err

if __name__ == "__main__":

    # Read orbital energy levels
    MO_en = read_MO_file(fMO)

    # Initialize fermi level guesses
    ef_left = min(MO_en)
    ef_right = max(MO_en)
    ef_mid = (ef_left + ef_right)/2
    #efs = [ef_left, ef_right, ef_mid]
    efs = [ef_left, ef_mid, ef_right]
    print efs

    thres = 1e3
    for _ in range(50):
        error = [0.0 for i in range(len(efs))]
        for i in range(len(efs)):
            err = fd_2_err(MO_en, efs[i], T)
            error[i] = err
#        print "error =",error

        # Use left half
        if error[0] < error[2]:
            efs[2] = efs[1]
            efs[1] = (efs[0] + efs[1])/2

        # Use right half
        elif error[0] > error[2]:
            efs[0] = efs[1]
            efs[1] = (efs[0] + efs[2])/2

        # If stuck, move the center position a random distance
        elif error[0] == error[2]:
            r = random.uniform(0.20, 0.80)
            efs[1] = (r*efs[0] + (1-r)*efs[2])

    print "efs =", efs

    fi_final = fermi_dirac(MO_en, efs[1], T)
    print fi_final, "Total elec =", np.sum(fi_final)
