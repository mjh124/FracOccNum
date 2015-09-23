#!/usr/bin/python

import sys
import numpy as np
import random

if len(sys.argv) != 4:
    print "Usage: Ef_calc_direct.py MO-file num-electrons temperature"
    exit(0)

fMO = sys.argv[1]
Nelec = int(sys.argv[2])
T = int(sys.argv[3])

def read_MO_file(fMO):

    MO_en = []
    with open(fMO) as f:
        lines = f.readlines()
    for line in lines:
        MO_en.append(float(line.split()[1]))
    return MO_en

def fermi_dirac(MO_en, ef, T):

    k = 3.1668114e-6 #[Ha/K]
    fi = []
    for i in range(len(MO_en)):
        tmp = np.exp((MO_en[i] - ef)/(k*T))
        fi.append(1/(1+tmp))
    return fi


def fd_2_err(MO_en, ef, T):

    fi_new = fermi_dirac(MO_en, ef, T)
    calc_elec = np.sum(fi_new)
    err = (calc_elec - Nelec)**2
    return err

def exit_routine(MO_en, ef, T):

    fi_final = fermi_dirac(MO_en, efs[1], T)
    print fi_final, "Total electrons =", np.sum(fi_final)
    print "Fermi Level =", efs[1]
    exit("Ef found successfully")

if __name__ == "__main__":

    MO_en = read_MO_file(fMO)

    # Initialize starting fermi level bounds
    ef_left = MO_en[Nelec-1]
    ef_right = MO_en[Nelec+1]
    ef_mid = (ef_left + ef_right) / 2
    efs = [ef_left, ef_mid, ef_right]
    print efs

    thres = 1e-12
    Niter = 0
    for _ in range(500):
        error = [0.0 for i in range(len(efs))]
        for i in range(len(efs)):
            err = fd_2_err(MO_en, efs[i], T)
            error[i] = err
        print "error =", error

        if error[1] <= thres:
            exit_routine(MO_en, efs[1], T)

        else:
            if error[0] < error[2]:
                efs[2] = (efs[1] + efs[2]) / 2
                efs[1] = (efs[0] + efs[2]) / 2

            elif error[0] > error[2]:
                efs[0] = (efs[0] + efs[1]) / 2
                efs[1] = (efs[0] + efs[2]) / 2

        Niter += 1
        print "Fermi window =", efs, "Number of iterations =", Niter

    print "Fermi Energy DID NOT CONVERGE"
