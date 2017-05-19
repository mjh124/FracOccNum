#!/usr/bin/python

import sys
import numpy as np

if len(sys.argv) != 3:
    print "Usage: FermiDiracDist.py fermi-energy temperature"
    exit(0)

ef = float(sys.argv[1])
T = int(sys.argv[2])

def fermi_dirac(MO_en, ef, T):

    k = 3.1668114e-6 #[Ha/K]
    fi = []
    for i in range(len(MO_en)):
        tmp = np.exp((MO_en[i] - ef)/(k*T))
        fi.append(1/(1+tmp))
    return fi

if __name__ == "__main__":

    #MO_en = [-0.224, -0.171, -0.065, -0.030, 0.024]
    MO_en = [-0.167, -0.123, -0.038, -0.002, 0.034]
    occ = fermi_dirac(MO_en, ef, T)
    print occ
