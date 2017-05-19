#!/usr/bin/python

import sys, os
import numpy as np
from scipy.optimize import minimize
from subprocess import check_call, check_output

if len(sys.argv) != 5:
    print "Usage: Topt_FONaSimplex.py filename total#Orbs #ActiveSpaces HOMO_idx(PYindexing)"
    exit(0)

filename = sys.argv[1].strip()[:-3]
tot_orbs = int(sys.argv[2])
Nas = int(sys.argv[3])
HOMO_idx = int(sys.argv[4])

def run_qchem(filename):

    qchem = "runqchem.sh"
    input = filename + ".in"
    output = filename + ".out"
    args = input + " " + output
    print(qchem, args)
    check_call([qchem, args])
    return output

def write_FONa(Norbs, Nel, temps, orb1, orb2):

    fn_FON = "FONa.dat"
    with open(fn_FON, 'w') as f:
        for i in range(len(temps)):
            f.write("%d %d %12.4f %d %d\n" % (Norbs[i], Nel[i], temps[i], orb1[i], orb2[i]))

def write_FONa1(Norbs, Nel, temps, occ_idx, Nas, virt_space):

    virt_idx = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    fn_FON = "FONa.dat"
    with open(fn_FON, 'w') as f:
        for i in range(len(Norbs)):
            f.write("%d %d %12.4f %d " % (Norbs[i], Nel[i], temps[i], occ_idx[i]))
            for j in virt_space:
                f.write("%d " % (j))
            f.write("\n")

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

def convergence_check(filename):

    # Not sure if I am going to use this yet
    message = "Have a nice day."
    conv = False
    with open(filename, 'r') as f:
        for line in f:
            if message in line:
                conv = True
            else:
                continue
    return conv

def energy(temps, Norbs, Nel, orb1, orb2, filename):

    write_FONa(Norbs, Nel, temps, orb1, orb2)
    run_qchem(filename)

    fn_out = filename + ".out"
    E = extract_CISDenergy(fn_out)

    return E

def energy1(temps, Norbs, Nel, occ_idx, Nas, filename, virt_space):

    write_FONa1(Norbs, Nel, temps, occ_idx, Nas, virt_space)
    run_qchem(filename)

    fn_out = filename + ".out"
    E = extract_CISDenergy(fn_out)

    return E

def get_args(tot_orbs, Nas, HOMO_idx):

    orbs = tot_orbs - HOMO_idx
    el = 2
    Norbs = []
    Nel = []
    occ_idx = []
    for i in range(Nas):
        Norbs.append(orbs)
        Nel.append(el)
        occ_idx.append(HOMO_idx-i)
    print Norbs, Nel, occ_idx

    return Norbs, Nel, occ_idx

def get_virt_space(tot_orbs, HOMO_idx):

    virt_space = []
    space_size = tot_orbs - HOMO_idx - 1
    for i in range(space_size):
        virt_orb = HOMO_idx + i + 1
        virt_space.append(virt_orb)
    return virt_space

def print_energy(x):

    outfile = filename + ".out"
    e = extract_CISDenergy(outfile)
    print("energy = %20.10f" % e)
    print x

def main():

    print("\n")
    print("---------------------------------------------------------")
    print("--  Optimize Parameters in Multi Active Space BEOS-SD  --")
    print("---------------------------------------------------------")

    #Setup and run qchem calculation, get energy
    x0 = [10000., 40000.]

    virt_space = get_virt_space(tot_orbs, HOMO_idx)
    Norbs, Nel, occ_idx = get_args(tot_orbs, Nas, HOMO_idx)

    #Norbs = [22, 22, 22]
    #Nel = [2, 2, 2]
    #occ_idx = [4, 5, 6]

    # Took this from DL, change where necessary
    #res = minimize(energy, x0, args=(Norbs, Nel, orb1, orb2, filename), jac=None, method='nelder-mead', options={'disp':True, 'xtol': 1, 'maxiter':100000}, callback=print_energy)
    res = minimize(energy1, x0, args=(Norbs, Nel, occ_idx, Nas, filename, virt_space), jac=None, method='nelder-mead', options={'disp':True, 'xtol': 1, 'maxiter':100000}, callback=print_energy)


if __name__ == "__main__":
    main()
