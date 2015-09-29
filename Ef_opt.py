#!/usr/bin/python

import sys
import numpy as np
import random

if len(sys.argv) != 5:
    print "Usage: Ef_calc_direct.py MO-file num-alpha-elec num-beta-elec temperature"
    exit(0)

fMO = sys.argv[1]
Nelec_alpha = int(sys.argv[2])
Nelec_beta = int(sys.argv[3])
T = int(sys.argv[4])

def read_MO_file(fMO):

    MO_en_alpha = []
    MO_en_beta = []
    with open(fMO) as f:
        lines = f.readlines()
    for line in lines:
        MO_en_alpha.append(float(line.split()[1]))
        if len(line.split()) == 3:
            MO_en_beta.append(float(line.split()[2]))
    return MO_en_alpha, MO_en_beta

def fermi_dirac(MO_en, ef, T):

    k = 3.1668114e-6 #[Ha/K]
    fi = []
    for i in range(len(MO_en)):
        tmp = np.exp((MO_en[i] - ef)/(k*T))
        fi.append(1/(1+tmp))
    return fi

def fd_2_err(MO_en, ef, Nelec, T):

    fi_new = fermi_dirac(MO_en, ef, T)
    calc_elec = np.sum(fi_new)
    err = (calc_elec - Nelec)**2
    return err

def find_initial_bounds(MO_en, Nelec, T):

    ef_left = MO_en[Nelec-1]
    ef_right = MO_en[Nelec]
    ef = (ef_left + ef_right) / 2
    fi = fermi_dirac(MO_en, ef, T)
    Nelec_calc = np.sum(fi)

    if Nelec - Nelec_calc >= 0:
        while Nelec - Nelec_calc >= 0:
            ef_right = ef_right + 1.0
            ef = (ef_left + ef_right) / 2
            fi = fermi_dirac(MO_en, ef, T)
            Nelec_calc = np.sum(fi)
        return ef_left, ef_right

    elif Nelec - Nelec_calc < 0:
        while Nelec - Nelec_calc < 0:
            ef_left = ef_left - 1.0
            ef = (ef_left + ef_right) / 2
            fi = fermi_dirac(MO_en, ef, T)
            Nelec_calc = np.sum(fi)
        return ef_left, ef_right

def exit_routine(MO_en, ef, T):

    fi_final = fermi_dirac(MO_en, efs[1], T)
    print fi_final, "Total electrons =", np.sum(fi_final)
    print "Fermi Level =", efs[1]
    exit("Ef found successfully")

def get_fermi_energy(MO_en, Nelec, T):

    # Initialize starting fermi level bounds
    ef_left, ef_right = find_initial_bounds(MO_en, Nelec, T)
    ef_mid = (MO_en[Nelec-1] + MO_en[Nelec]) / 2
    efs = [ef_left, ef_mid, ef_right]
#    print efs

    thres = 1e-20
    Niter = 0
    for _ in range(100):
        error = [0.0 for i in range(len(efs))]
        for i in range(len(efs)):
            err = fd_2_err(MO_en, efs[i], Nelec, T)
            error[i] = err
#        print "error =", error

        if error[1] <= thres:
            fi_final = fermi_dirac(MO_en, efs[1], T)
            return fi_final, efs[1]

        else:
            if error[0] < error[2]:
                efs[2] = (efs[1] + efs[2]) / 2
                efs[1] = (efs[0] + efs[2]) / 2

            elif error[0] > error[2]:
                efs[0] = (efs[0] + efs[1]) / 2
                efs[1] = (efs[0] + efs[2]) / 2

        Niter += 1
#        print "Fermi =", efs[1], "Number of iterations =", Niter

    return "Fermi Energy DID NOT CONVERGE"

if __name__ == "__main__":

    MO_en_alpha, MO_en_beta = read_MO_file(fMO)

    alpha = get_fermi_energy(MO_en_alpha, Nelec_alpha, T)
    if len(alpha) == 2:
        print "fi_alpha =", alpha[0], ", Nelec_alpha =", np.sum(alpha[0]), ", alpha_Ef =", alpha[1]
    else:
        print "Alpha fermi energy did not converge"

    if Nelec_beta != 0:
        beta = get_fermi_energy(MO_en_beta, Nelec_beta, T)
        if len(beta) == 2:
            print "fi_beta =", beta[0], ", Nelec_beta =", np.sum(beta[0]), ", beta_Ef =", beta[1]
        else:
            print "Beta fermi energy did not converge"
