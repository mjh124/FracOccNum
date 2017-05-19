#!/usr/bin/python

# Script to variationally minimize the energy w.r.t. temperature

import sys, os
import numpy as np
from scipy.optimize import minimize
from subprocess import check_call, check_output

if len(sys.argv) != 7:
        print "Usage: Topt_FON_unres.py qchem-input #AS tot_a_orbs tot_b_orbs aHOMO bHOMO"
        exit(0)

filename = sys.argv[1].strip()[:-3]
num_AS = int(sys.argv[2])
num_aOrbs = int(sys.argv[3])
num_bOrbs = int(sys.argv[4])
aHOMO = int(sys.argv[5])
bHOMO = int(sys.argv[6])

###
# Run qchem
###

def run_qchem(filename):

    qchem = "runqchem.sh"
    input = filename + ".in"
    output = filename + ".out"
    args = input + " " + output
    print(qchem, args)
    check_call([qchem, args])
    return output

###
# Check for convergence
###

def convergence_check(filename):

    f = filename + ".out"
    outfile = open(f, 'r')
    outlines = outfile.readlines()
    outfile.close()
    message = "Have a nice day."

    conv = False
    for line in outlines:
        if message in line:
            conv = True
        else:
            continue

    return conv

###
# Write FON?.dat files
###

def write_FONa(num_AS, num_aOrbs, alpha_temps, occ_aidx, virt_alpha):

    fn_FON = "FONa.dat"
    aOrbs = []
    num_aElec = []
    for i in range(num_AS):
        aOrbs.append(len(virt_alpha)+1)
        num_aElec.append(2)
    with open(fn_FON, 'w') as f:
        for i in range(num_AS):
            f.write("%d %d %12.4f %d " % (aOrbs[i], num_aElec[i], alpha_temps[i], occ_aidx[i]))
            for j in virt_alpha:
                f.write("%d " % (j))
            f.write("\n")

def write_FONb(num_AS, num_bOrbs, beta_temps, occ_bidx, virt_beta):

    fn_FON = "FONb.dat"
    bOrbs = []
    num_bElec = []
    for i in range(num_AS):
        bOrbs.append(len(virt_beta)+1)
        num_bElec.append(2)
    with open(fn_FON, 'w') as f:
        for i in range(num_AS):
            f.write("%d %d %12.4f %d " % (bOrbs[i], num_bElec[i], beta_temps[i], occ_bidx[i]))
            for j in virt_beta:
                f.write("%d " % (j))
            f.write("\n")

###
# Extract CISD energy
###

def extract_CISDenergy(filename):

    message = "Total energy ="
    states = []
    with open(filename, 'r') as f:
        for line in f:
            if message in line:
                states.append(float(line.split()[3]))
    if len(states) == 0:
        energy = 1e5
    else:
        energy = states[0]
    return energy

def get_alpha_args(num_AS, num_aOrbs, aHOMO):

    lumo = aHOMO + 1
    virt_alpha = np.arange(lumo, num_aOrbs)
    occ_aidx = []
    for i in range(num_AS):
        occ_aidx.append(aHOMO-i)
    return occ_aidx, virt_alpha

def get_beta_args(num_AS, num_bOrbs, bHOMO):

    lumo = bHOMO + 1
    virt_beta = np.arange(lumo, num_bOrbs)
    occ_bidx = []
    for i in range(num_AS):
        occ_bidx.append(bHOMO-i)
    return occ_bidx, virt_beta

def energy(temps, num_AS, num_aOrbs, num_bOrbs, occ_aidx, occ_bidx, virt_alpha, virt_beta, filename):

    alpha_temps = []
    beta_temps = []
    for i in range(len(temps)):
        if i % 2 == 0:
            alpha_temps.append(temps[i])
        else:
            beta_temps.append(temps[i])

    write_FONa(num_AS, num_aOrbs, alpha_temps, occ_aidx, virt_alpha)
    write_FONb(num_AS, num_bOrbs, beta_temps, occ_bidx, virt_beta)
    run_qchem(filename)

    fn_out = filename + ".out"
    E = extract_CISDenergy(fn_out)
    return E

def print_energy(x):

    outfile = filename + ".out"
    e = extract_CISDenergy(outfile)
    print("energy = %20.10f" % e)
    print x

def main():

    print("\n")
    print("------------------------------------------------------------------------")
    print("--  Optimize Parameters in Multi Active Space Unrestricted DM1D-CISD  --")
    print("------------------------------------------------------------------------")

    x0 = [10000, 15000, 10000, 15000]

    alpha_temps = []
    beta_temps = []
    for i in range(len(x0)):
        if i % 2 == 0:
            alpha_temps.append(x0[i])
        else:
            beta_temps.append(x0[i])

    occ_aidx, virt_alpha = get_alpha_args(num_AS, num_aOrbs, aHOMO)
    occ_bidx, virt_beta = get_beta_args(num_AS, num_bOrbs, bHOMO)
    write_FONa(num_AS, num_aOrbs, alpha_temps, occ_aidx, virt_alpha)
    write_FONb(num_AS, num_bOrbs, beta_temps, occ_bidx, virt_beta)

if __name__ == "__main__":
    main()
