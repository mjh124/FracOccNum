#!/usr/bin/env python

# use python/anaconda-1.9.2-rhel

import sys
from subprocess import check_call, call
from scipy.optimized import minimize
import numpy as np
from math import erf

# Optimizes temperature for a FON calculation

# Things to change when implementing my functions
#   Input signature
#   Set up of the active spaces
#   Map out and reimplement Eocc/E optimization functions for active space pairs
# What functions do I need?
#   Function that takes the energy of the two orbitals in an active space and returns their occupations
#   Parser to couple orbital number to energy

usage = "fon_opt input-file Nfrz Nocc_alpha Nocc_beta Nbasis Nspaces Unrestricted T0 Nthread"

if len(sys.argv) != 10:
    print(usage)
    sys.exit(1)

fname = sys.argv[1]
Nfrz = int(sys.argv[2])
Nocc_alpha = int(sys.argv[3])
Nocc_beta = int(sys.argz[4])
Nbasis = int(sys.argv[5])
Nspaces = int(sys.argv[6])
Unrestricted = sys.argv[7]
Tini = float(sys.argv[8]) # in: Hartree
Nthread = int(sys.argv[9])

print "Nfrz =", Nfrz
print "Nocc_alpha =", Nocc_alpha
print "Nocc_beta =", Nocc_beta
print "Nbasis =", Nbasis
print "Nspaces =", Nspaces
print "Unrestricted =", Unrestricted

# Set up active spaces
spaces_alpha = []
spaces_beta = []

Nact_orbitals = Nbasis - Nfrz
Nact_alpha = Nocc_alpha - Nfrz
Nact_beta = Nocc_beta - Nfrz

# Rewrite the active space functions as needed
if Nspaces == 0:
# Builds the starting occupation number for each active space
    T0 = []

    for i in range(Nfrz, Nbasis):

        space_alpha = [1, 1, 1.000, i]
        space_beta = [1, 1, 1.000, i]

        T0.append(1.000)
        T0.append(1.000)

        if i >= Nocc_alpha:
            space_alpha = [1, 1, 0.000, i]
            T0[-2] = 0.000
        if i >= Nocc_beta:
            space_beta = [1, 1, 0.000, i]
            T0[-1] = 0.000

        spaces_alpha.append(space_alpha)
        spaces_beta.append(space_beta)

elif Nspaces == 1:
# Builds space with #Act_orbs, #Act_alpha, 1(not sure), and a list of active orbitals (same for beta)
    space = [Nact_orbitals, Nact_alpha, 1]
    for i in range(Nfrz, Nbasis):
        space.append(i)

    spaces_alpha.append(space)

    space = [Nact_orbitals, Nact_beta, 1]
    for i in range(Nfrz, Nbasis):
        space.append(i)
    spaces_beta.append(space)

    # initial temperature(s)
    T0 = [Tini, Tini]

elif Nspaces == 2:
# Builds all occupied - virtual orbital pairs for both alpha and beta (not implemented)
    for i in range(Nfrz, Nocc_alpha):
        for a in range(Nocc_alpha, Nbasis):
            space = [i, a]
            spaces.append(space)
    for i in range(Nfrz, Nocc_beta):
        for a in range(Nocc_beta, Nbasis):
            space = [i, a]
            spaces.append(space)

else:
    print "Nspaces =", Nspaces
    print "Not supported."
    sys.exit(1)

print "Active spaces:"
print(spaces_alpha)
print(spaces_beta)

def writeSpacesToDisk(spaces, alpha):
    file = "FONa.dat"
    if not alpha:
        file = "FONb.dat"

    f = open(file, 'w')

    for space in spaces:
        line = str(space[0]) + " " + str(space[1]) + " " + str(space[2]) + " "
        for i in range(3, len(space)):
            line += str(space[i]) + " "
        line += "\n"
        f.write(line)

    f.close()

def extract_energy(fname):

    fname2 = "test.out"
    f = open(fname2, 'r')

    converged = False
    for line in f:
        if "Convergence criterion met" in line:
            en = float(line.split()[1])
            converged = True

    f.close()

    if not converged:
        print "Q-Chem job did not converge. See ", fname2
        sys.exit(1)

    return en

def runqchem(fname):
    qchem = "runqchem.sh"
    input = fname
    output = "test.out"
    args = "-nt " + str(Nthread) + " " + input + " " + output
    check_call([qchem, args])

def get_occ_en(index, alpha):

    # Function that takes orbital index and returns energy
    spin = "Alpha MOs"
    if not alpha:
        spin = "Beta MOs"

    fname2 = "test.out"
    f = open(fname2, 'r')

    orb_en = 0.0
    for line in f:
        if spin in line:
            next(f)
            for line in f:
                if "Virtual" in line:
                    break
                tokens = line.split()
                if index <= len(tokens):
                    orb_en = tokens[index-1]
                    break
                else:
                    index -= 8
                    
    f.close()
    return orb_en

def En2Occ(T, occ_en, virt_en):

    k = 1.38e-23 # [J/K]
    k_ha = 3.1668114e-6 [Ha/K]
    F1tmp = 1
    F2tmp = np.exp((occ_en - virt_en)/(k_ha*T))
    F2 = F2tmp / (F2tmp + F1tmp)
    F1 = F1tmp / (F2tmp + F1tmp)
    return F1, F2

def Etemp(T):

    for i in range(len(T)):
        
        # Do something to build temperature

        writeSpacesToDisk(spaces_alpha, True)
        writeSpacesToDisk(spaces_beta, False)

        if Ta < 1 of Tb < 1:
            print("Penalizing step becasue of negative temperature.")
            return 1e6

        runqchem(fname)

        en = extract_energy(fname)

        print("    %3d  #20.10f  %10.1f  %10.1f  %10.6f  %10.6"  % (i, en, Ta, Tb, Ta_Eh, Tb_En))

        return en
