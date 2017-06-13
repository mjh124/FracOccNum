#!/usr/bin/python

import sys
import numpy as np

if len(sys.argv) != 5:
    print "Usage: build_RealSpace_CISDDensity.py Density-Matrix len-DM Natoms #total-orbitals"
    exit(0)

fn_DM = sys.argv[1]
Dpq_len = int(sys.argv[2])
Natoms = int(sys.argv[3])
tot_orbs = int(sys.argv[4])

def read_DensMat(fn_DM):

    Dpq = np.zeros((Dpq_len, Dpq_len))
    with open(fn_DM, 'r') as f:
        lines = f.readlines()[1:]
        for line in lines:
            tokens = line.split()
            Dpq[int(tokens[0])][int(tokens[1])] = float(tokens[2])
    return Dpq

def get_density(fn):

    density = []
    skip = Natoms + 6
    with open(fn, 'r') as f:
        lines = f.readlines()[skip:]
        for line in lines:
            tokens = line.split()
            for i in tokens:
                density.append(float(i))
    return density

def get_preamble(fn, Natoms):

    num_lines = 6 + Natoms
    with open(fn, 'r') as f:
        preamble = f.readlines()[:num_lines]
    idx1 = preamble[3].split()[0]
    idx2 = preamble[4].split()[0]
    idx3 = preamble[5].split()[0]
    return preamble, idx1, idx2, idx3

def idx2MO(idx, Nalpha, Nbeta, Nbasis, Nfroz):                                                               
    NAvirt = Nbasis - (Nalpha + Nfroz)
    NBvirt = Nbasis - (Nbeta + Nfroz)
    if idx < Nalpha:
        MO_idx = idx + 1 + Nfroz
#        print idx, 'alpha_occ', MO_idx
    elif idx >= Nalpha and idx < Nalpha+Nbeta:
        MO_idx = Nbasis + (idx-Nalpha) + 1 + Nfroz
#        print idx, 'beta_occ', MO_idx
    elif idx >= Nalpha+Nbeta and idx < Nalpha+Nbeta+NAvirt:
        MO_idx = idx-Nbeta + 1 + Nfroz
#        print idx, 'alpha_virt', MO_idx
    else: 
        MO_idx = idx + 1 + Nfroz + Nfroz
#        print idx, 'beta_virt', MO_idx
    return MO_idx

def extract_MOs(Ngrid, Norbs):

    orb_densities = np.zeros((Ngrid, Norbs))
    for i in range(Norbs):
        fn = 'mo.' + str(i+1) + '.cube'
        orb_dens = get_density(fn)
        for j in range(len(orb_dens)):
            orb_densities[j][i] = orb_dens[j]
    return orb_densities

def write_output(preamble, density):

    fn_out = fn_DM.strip()[:-11] + 'CISDDens.cube'
    with open(fn_out, 'w') as f:
        for i in range(len(preamble)):
            f.write("%s" % preamble[i])
        for i in range(len(density)):
            f.write("%.6e\n" % density[i])

if __name__ == "__main__":

    #Constants, These are specific to N2 with 6-31G basis
    Nalpha = 5
    Nbeta = 5
    Nbasis = 18
    Nfroz = 2

    Dpq = read_DensMat(fn_DM)
    #print Dpq

    fn = 'mo.1.cube'
    preamble, idx1, idx2, idx3 = get_preamble(fn, Natoms)
    print idx1, idx2, idx3
    Ngrid = int(idx1) * int(idx2) * int(idx3)

    orb_densities = extract_MOs(Ngrid, tot_orbs)
    print orb_densities.shape

    gamma = np.zeros((Ngrid))
    for r in range(Ngrid):
        Edens_r = 0.0

        if r % 1000 == 0:
            print 'calculating at',r,'th grid point'

        for p in range(len(Dpq)):
            MO_idx_p = idx2MO(p, Nalpha, Nbeta, Nbasis, Nfroz)
            for q in range(len(Dpq)):
                MO_idx_q = idx2MO(q, Nalpha, Nbeta, Nbasis, Nfroz)

                Edens_r += Dpq[p][q] * orb_densities[r][p] * orb_densities[r][q]

        gamma[r] = Edens_r

    write_output(preamble, gamma)
