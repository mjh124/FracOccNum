#!/usr/bin/python

# Script to variationally minimize the energy w.r.t. temperature

import sys, os
import numpy as np
from scipy.optimize import minimize
from subprocess import check_call, check_output

if len(sys.argv) != 8:
        print "Usage: Topt_fdFON_unres.py qchem-input tot_a_orbs tot_b_orbs aHOMO bHOMO aTemp bTemp"
        exit(0)

filename = sys.argv[1].strip()[:-3]
num_aOrbs = int(sys.argv[2])
num_bOrbs = int(sys.argv[3])
aHOMO = int(sys.argv[4])
bHOMO = int(sys.argv[5])
aTemp = float(sys.argv[6])
bTemp = float(sys.argv[7])

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

def write_FONa(num_aOrbs, aTemp, aHOMO):

    fn_FON = "FONa.dat"
    aOrbs = np.arange(num_aOrbs)
    num_aElec = aHOMO
    with open(fn_FON, 'w') as f:
        f.write("%d %d %12.4f " % (len(aOrbs), num_aElec, aTemp))
        for j in aOrbs:
            f.write("%d " % (j))

def write_FONb(num_bOrbs, bTemp, bHOMO):

    fn_FON = "FONb.dat"
    bOrbs = np.arange(num_bOrbs)
    num_bElec = bHOMO
    with open(fn_FON, 'w') as f:
        f.write("%d %d %12.4f " % (len(bOrbs), num_bElec, bTemp))
        for j in bOrbs:
            f.write("%d " % (j))

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

def energy(temps, num_aOrbs, num_bOrbs, aHOMO, bHOMO, filename):

    aTemp = temps[0]
    bTemp = temps[1]

    write_FONa(num_aOrbs, aTemp, aHOMO)
    write_FONb(num_bOrbs, bTemp, bHOMO)
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
    print("----------------------------------------------------------------------------")
    print("--  Optimize Parameters of Single Active Space Unrestricted FD DM1D-CISD  --")
    print("----------------------------------------------------------------------------")

    x0 = [aTemp, bTemp]

    res = minimize(energy, x0, args=(num_aOrbs, num_bOrbs, aHOMO, bHOMO, filename), jac=None, method='nelder-mead', options={'disp':True, 'xtol':1, 'maxiter':100000}, callback=print_energy)

if __name__ == "__main__":
    main()
