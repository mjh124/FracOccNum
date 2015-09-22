#!/usr/bin/env python

# use python/anaconda-1.9.2-rhel

import sys
from subprocess import check_call, call
from scipy.optimize import minimize
import numpy as np
from math import erf

# Optimizes temperature for a FON calculation

usage = "fon_opt  input-file  Nfrz  Nocc_alpha  Nocc_beta  Nbasis  Nspaces  Unrestricted  T0  Nthread"

if len(sys.argv) != 10:
    print(usage)
    sys.exit(1)


fname = sys.argv[1]
Nfrz = int(sys.argv[2])
Nocc_alpha = int(sys.argv[3])
Nocc_beta = int(sys.argv[4])
Nbasis = int(sys.argv[5])
Nspaces = int(sys.argv[6])
Unrestricted = sys.argv[7]
Tini = float(sys.argv[8]) # in: Hartree 
Nthread = int(sys.argv[9])


print "Nfrz = ", Nfrz
print "Nocc_alpha = ", Nocc_alpha
print "Nocc_beta = ", Nocc_beta
print "Nbasis = ", Nbasis
print "Nspaces = ", Nspaces
print "Unrestricted = ", Unrestricted

# Set up active spaces
spaces_alpha = []
spaces_beta = []

Nact_orbitals = Nbasis - Nfrz
Nact_alpha = Nocc_alpha - Nfrz
Nact_beta = Nocc_beta - Nfrz

if Nspaces == 0:

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

    for i in range(Nfrz, Nocc_alpha):
        for a in range(Nocc_alpha, Nbasis):
            space = [i, a]
            spaces.append(space)
    for i in range(Nfrz, Nocc_beta):
        for a in range(Nocc_beta, Nbasis):
            space = [i, a]
            spaces.append(space)

else:
    print "Nspaces = ", Nspaces
    print "Not supported."
    sys.exit(1)

print "Active spaces:"
print(spaces_alpha)
print(spaces_beta)


def writeSpacesToDisk(spaces, alpha):
    file = "FONa.dat"
    if not alpha:
        file = "FONb.dat"

    f = open(file, "w")

    for space in spaces:
        line = str(space[0]) + " " + str(space[1]) + " " + str(space[2]) + " "
        for i in range(3, len(space)):
            line += str(space[i]) + " "
        line += "\n"
        f.write(line)

    f.close()

def extract_energy(fname):
    fname2 = "test.out"

    f = open(fname2, "r")

    converged = False
    for line in f:
        if "Convergence criterion met" in line:
            en = float(line.split()[1])
            converged = True

    f.close()

    if not converged:
        print "Q-Chem job did not converge. See ", fname2
        sys.exit(1)

    #print("E = %20.10f" % en)
    return en

def runqchem(fname):
    qchem = "runqchem.sh"
    input = fname
    output = "test.out"
    #args = input + " " + output + " " + str(Nthread)
    args = "-nt " + str(Nthread) + " " + input + " " + output
    #args = [input, output, str(Nthread)]
    #print(qchem, args)
    #subprocess.check_output([qchem,args])
    check_call([qchem,args])
    #call(qchem, 'h2o.in', shell=False)



def E(T):
    for i in range(len(T)):
        #Ta = 300 + (int(T[2*i]) - 300)*1
        #Tb = 300 + (int(T[2*i+1]) - 300)*1
        #print("%.6e   %.6e" % (D[2*i], D[2*i+1]))
        Ta_Eh = T[2*i]
        Tb_Eh = T[2*i+1]
        Ta = Ta_Eh * 315775 # Hartree -> Kelvin
        Tb = Tb_Eh * 315775 # Hartree -> Kelvin
        spaces_alpha[i][2] = Ta
        spaces_beta[i][2] = Tb


        writeSpacesToDisk(spaces_alpha, True)
        writeSpacesToDisk(spaces_beta, False)

        if Ta < 1 or Tb < 1:
            print("Penalizing step because of negative temperature.")
            return 1e6

        runqchem(fname)

        en = extract_energy(fname)

        print("    %3d   %20.10f   %10.1f   %10.1f   %10.6f   %10.6f" % (i, en, Ta, Tb, Ta_Eh, Tb_Eh))

        return en

def Eocc(T):

    Niter = 0

    occ_alpha = ""
    occ_beta = ""
    for i in range(len(T)/2):
        #Ta = 300 + (int(T[2*i]) - 300)*1
        #Tb = 300 + (int(T[2*i+1]) - 300)*1
        #print("%.6e   %.6e" % (D[2*i], D[2*i+1]))
        Ta = T[2*i]
        Tb = T[2*i+1]

        occ_alpha += str(Ta) + " "
        occ_beta += str(Tb) + " "

        spaces_alpha[i][2] = Ta
        spaces_beta[i][2] = Tb

        #if Ta < 0 or Tb < 0 or Ta > 1 or Tb > 1:
        #    print("*** Warning: Occupation(s) outside allowed range!")
        #    print("*** occ[%d]:   %10.3f alpha   %10.3f beta" % (i, Ta, Tb))

    writeSpacesToDisk(spaces_alpha, True)
    writeSpacesToDisk(spaces_beta, False)

    runqchem(fname)

    en = extract_energy(fname)

    Niter += 1

    # Parameters for enforcing constraints
    alpha = 1.e4 # steepness of occupation penalty function
    lm_1 = 1e3
    lm_2 = 1
    occ_tol = 1e-3
    one = 1.0 + occ_tol
    zero = 0.0 - occ_tol

    N_alpha = 0
    N_beta = 0
    for i in range(len(T)/2):
        N_alpha += T[2*i]
        N_beta += T[2*i+1]
    N_total = N_alpha + N_beta
    N_act = Nact_alpha + Nact_beta
    penalty = lm_1 * ((N_alpha - Nact_alpha)**2.0 + (N_beta - Nact_beta)**2.0)
    #penalty = lm_1 * (N_total - N_act)**2.0 
    #if penalty > 0.1:
    #    print("    N_alpha = %10.6f   N_beta = %10.6f   penalty = %16.6e" % (N_alpha, N_beta, penalty))
    en += penalty

    penalty_alpha = 0.0
    penalty_beta = 0.0
    for i in range(len(T)/2):
        x = T[2*i]
        y = T[2*i+1]
        a = (0.5 * (erf(alpha*(x - one)) + erf(alpha*(x - zero))))**2.0
        b = (0.5 * (erf(alpha*(y - one)) + erf(alpha*(y - zero))))**2.0
        penalty_alpha += a
        penalty_beta += b
        #if a > 0.1 or b > 0.1:
        print("      occ[%d]:   %10.6e   %10.6e   %10.3e   %10.3e" % (i,x,y,a,b))
    en += lm_2 * (penalty_alpha + penalty_beta)
    #print("      alpha occupation penalty:  %20.10e" % penalty_alpha)
    #print("      beta occupation penalty:  %20.10e" % penalty_beta)

    print("    %3d   %20.10f   %10.6f   %10.6f   %10.3e   %10.3e   %10.3e" % (Niter, en, N_alpha, N_beta, penalty, penalty_alpha, penalty_beta))
    print("                                  %s" % (occ_alpha))
    print("                                  %s" % (occ_beta))


    return en

if Nspaces == 0:

    print "*** Optimizing E(f1, f2, ...) ***"

    print("-- Active Space Occupation Optimization --")
    print("It. No.                 Energy     Alpha / Beta Occupations ")

    #cons = ({'type': 'eq',
    #         'fun': lambda x: np.array( np.sum(x) - Nact_alpha - Nact_beta)})
    cons = ({'type': 'ineq',
             'fun': lambda x: np.array( 1 - x[0] )},
            {'type': 'ineq',
             'fun': lambda x: np.array( 1 - x[1] )},
            {'type': 'ineq',
             'fun': lambda x: np.array( x[0] )},
            {'type': 'ineq',
             'fun': lambda x: np.array( x[1] )},
           )

    #minimize(Eocc, T0, method='COBYLA', options={'disp': True, 'catol': 1e-6}, constraints=cons)
    minimize(Eocc, T0, method='Nelder-Mead', options={'disp': True})

    # print final parameters

elif Nspaces == 1:
    print "*** Optimizing E(T) ***"



    #cons = ({'type': 'ineq', 'fun': lambda x:  x[0] + 2 * x[1] + 2},
    bnds = ((0, None), (0, None))
    print("-- Active Space Temperature Optimization --")
    print("Space #                 Energy     Alpha (K)     Beta (K)   Alpha (Eh)    Beta (Eh)")
    #minimize(E, T0, method='Nelder-Mead', options={'disp': True})
    #minimize(E, T0, method='Powell', options={'disp': True})
    minimize(E, T0, method='COBYLA', options={'disp': True})
    #minimize(E, T0, method='SLSQP', options={'disp': True}, bounds=bnds)
    #minimize(E, T0, method='Nelder-Mead', options={'disp': True}, bounds=bnds)
    #scipy.optimize.minimize(E, T0, method='Nelder-Mead')

else:
    print "Nspaces = ", Nspaces
    print "Not supported."
    sys.exit(1)
