#!/usr/bin/python

import sys
import re
import numpy as np

if len(sys.argv) != 3:
    print "Usage: build_enLevel_gnuplot.py BL temps"
    print " Warning, MO parsing is written specifically for N2"
    exit(0)

BL = sys.argv[1]
temps = sys.argv[2]

def get_MOs(fn_qchem, virt=0):

    message = "-- Occupied --"
    breaker = "-- Virtual --"
    if virt > 0:
        message = "-- Virtual --"
        breaker = "Beta MOs"

    count = 0
    orb_line = ""
    with open(fn_qchem, 'r') as f:
        for line in f:
            if message in line:
                count += 1
                if count != 5:
                    continue
                else:
                    for line in f:
                        if breaker in line:
                            break
                        orb_line += line

    N2_Occ = []
    tokens = orb_line.split()
    if virt == 0:
        for i in range(2, 7):
            N2_Occ.append(float(tokens[i]))
    else:
        for i in range(3):
            N2_Occ.append(float(tokens[i]))

    return N2_Occ

def get_Ef(fn_qchem):

    Efs = []
    with open(fn_qchem, 'r') as f:
        for line in f:
            if "Fermi level =" in line:
                Efs.append(float(line.split()[3]))
    Ef = Efs[-1]
    return Ef

#def calculate_ONs(temp, MOs, Ef):
#
#    beta = 1.0e0 / (k*temp)
#    ONs = np.zeros(len(MOs))
#    for i in range(len(MOs)):
#        denom = 1.0 + np.exp(beta * (MOs[i] - Ef))
#        NOs[i] = 1.0e0/denom
#    return ONs

def split_temps(temps):

    Ts = []
    tmp = re.split(',', temps)
    print tmp
    for i in range(len(tmp)):
        Ts.append(int(tmp[i]))
    return Ts

if __name__ == "__main__":

    Ts = split_temps(temps)
    print Ts

    for j in range(len(Ts)):

        s = 0.2 + j
        e = 0.8 + j

        print '# %dK\n' % Ts[j]
        fn_qchem = 'N2_' + str(BL) + 'A_' + str(Ts[j]) + 'K.out'
        MO_OccEns = get_MOs(fn_qchem)
        MO_VirtEns = get_MOs(fn_qchem, virt=1)
        MOs = MO_OccEns + MO_VirtEns
        #print MO_OccEns, MO_VirtEns
        #print MOs
    
        Ef = get_Ef(fn_qchem)
        #print Ef
    
        for i in range(len(MOs)):
            energy = MOs[i] - Ef
            print 'set arrow from %2.1f,%8.6f to %2.1f,%8.6f nohead lt 1 lc -1 lw 4' % (s, energy, e, energy)

        print '\n'
