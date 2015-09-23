import numpy as np
import random

def read_MO_file(fMO):
''' Read in Molecular orbital file '''

    MO_en = []
    with open(fMO) as f:
        lines = f.readlines()
    for line in lines:
            MO_en.append(float(line.split()[1]))
        return MO_en

def fermi_dirac(MO_en, ef, T):
''' Calculate the occupations of a list of MOs
    based on a fermi dirac distribution '''

    k = 3.1668114e-6 #[Ha/K]
    fi = []
    for i in range(len(MO_en)):
        tmp = np.exp((MO_en[i] - ef)/(k*T))
        fi.append(1/(1+tmp))
    return fi


def fd_2_err(MO_en, ef, T):
''' Calculate the error in occupation number from a 
    fermi dirac distribution and return error to minimize '''

    fi_new = fermi_dirac(MO_en, ef, T)
    calc_elec = np.sum(fi_new)
    err = (calc_elec - Nelec)**2
    return err

def exit_routine(MO_en, ef, T):
''' Exit routine once convergence criterion is meet '''

    fi_final = fermi_dirac(MO_en, efs[1], T)
    print fi_final, "Total electrons =", np.sum(fi_final)
    print "Fermi Level =", efs[1]
    exit("Ef found successfully")

def get_fermi_energy(fMO, Nelec, T):
''' Iteratively calculate the fermi energy '''

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
        print "Fermi window =", efs, "Number of iterations =", Niter

    return "Fermi Energy DID NOT CONVERGE"
