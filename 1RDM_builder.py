#!/usr/bin/python

import sys
import copy
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

if len(sys.argv) != 4:
    print "Usage: 1RDM_builder.py Nbasis Nalpha Nbeta"
    print "    Nbasis-total#orbs (alpha+beta), Nalphs(Nbeta)-#alpha(beta)electrons"
    print "    exitation-level is 0, 1, or 2 for HF, HF+S, or HF+S+D, respectively"
    print "    Assuming a spin orbital basis with order a,abar,b,bbar,...,N,Nbar"
    exit(0)

Nbasis = int(sys.argv[1])
Nalpha = int(sys.argv[2])
Nbeta = int(sys.argv[3])
#ex_level = int(sys.argv[4])

def form_HF_det(Nbasis, Nalpha, Nbeta):

    ON_hf = [0 for i in range(Nbasis)]
    tot_el = Nalpha + Nbeta
    for i in range(Nbasis):
        if i < tot_el:
            ON_hf[i] = 1
    return ON_hf

def do_excitation(ON, chi):

    # chi is a 2x1 array where [0] is annihilation and [1] is creation orb
#    if chi[0] % 2 == chi[1] % 2:
    if ON[chi[0]] == 1 and ON[chi[1]] == 0:
        ON[chi[0]] = 0
        ON[chi[1]] = 1
    else:
        ON = [0 for i in range(len(ON))]
#    else:
#        ON = [0 for i in range(len(ON))]
    return ON

def form_singles_WF(ON):

    # chi is a 2x1 array where [0] is annihilation and [1] is creation orb
    singles = []
    for i in range(Nbasis):
        for j in range(Nbasis):
            chi = [i, j]
            ONHF = form_HF_det(Nbasis, Nalpha, Nbeta)
            ON_ex = do_excitation(ONHF, chi)
            if sum(ON_ex) > 0:
                singles.append(ON_ex)
    return singles

def form_doubles_WF(ON, Nelec):

    chis = []
    for i in range(Nbasis):
        for j in range(Nbasis):
            chi = [i, j]
            chis.append(chi)
    #print chis
    doubles = []
    for i in chis:
        for j in chis:
            if i[0] != j[0] and i[1] != j[1]: # Can't excite from or into same orbital
                ON_tmp = copy.deepcopy(ON)
                ON_sing = do_excitation(ON_tmp, i)
	        if np.sum(ON_sing) == Nelec:
                    #print ON_sing, np.sum(ON_sing)
                    ON_doub = do_excitation(ON_sing, j)
                    singles = sum(ON_doub[:Nelec])
	            if singles == Nelec-2:
                        if ON_doub in doubles:
                            continue
                        #print ' ',ON_doub, np.sum(ON_doub)
                        doubles.append(ON_doub)
    return doubles

def get_amplitude(vec):

    annih = []
    create = []
    ON = form_HF_det(Nbasis, Nalpha, Nbeta)
    for i in range(Nbasis):
        vec_diff = ON[i] - vec[i]
        if vec_diff == 1:
            annih.append(i)
        elif vec_diff == -1:
            create.append(i)
    return annih, create

if __name__ == "__main__":

    # Generate HF ON string
    Nelec = Nalpha + Nbeta
    ON = form_HF_det(Nbasis, Nalpha, Nbeta)
    ON_hf = []
    ON_hf.append(form_HF_det(Nbasis, Nalpha, Nbeta))
    singles = form_singles_WF(ON)
    doubles = form_doubles_WF(ON, Nelec)
    #for i in range(len(doubles)):
    #    print doubles[i]

    # Eventually insert excitation level here to merge desired level of theory
    #bra = ON_hf + singles + doubles
    bra = ON_hf
    #ket = ON_hf + singles + doubles
    ket = singles
#    for i in range(len(bra)):
#        print bra[i], ket[i]

    #D = [[0 for p in range(Nbasis)] for q in range(Nbasis)] #Initialize density matrix
    D = np.zeros((Nbasis, Nbasis))
    for p in range(Nbasis):
        for q in range(Nbasis):
            # form the matrix elements, Dpq = <psi|a+_pa_q|psi>
            Dpq = 0
            bra_tmp = copy.deepcopy(bra)
            for i in bra_tmp:
                i_tmp = copy.deepcopy(i)
                ket_tmp = copy.deepcopy(ket)
                for j in ket_tmp:

                    j_tmp = copy.deepcopy(j)

                    if j[q] != 1:
                        dij = 0 #Screens for possible excitations, takes care of delta_q because it operates first...need to do excitation before calculating delta_p

                    else:

                        #Perform excitation, first remove an electron from q then add one to p
                        gamma_q = 1
			for k in range(0, q):
                            gamma_q *= (-1)**(j[k])

                        delta_q = 1 #Condition above ensures this
                        j[q] = 0

                        gamma_p = 1
			for k in range(0, p):
                            gamma_p *= (-1)**(j[k])

                        delta_p = 0
                        if j[p] == 0: 
                            delta_p = 1
                            j[p] = 1

                        #Calculate overlap between ON vectors <Ki|Kj_qp>
                        ON_overlap = 1
                        for k in range(Nbasis):
                            if i[k] != j[k]:
                                ON_overlap = 0

                        #Bring everything together
                        dij = delta_p * delta_q * gamma_p * gamma_q * ON_overlap #This is true for p > q
                        dij = delta_p * delta_q * gamma_p * gamma_q * ON_overlap #* Amp[Bra key] * Amp[Ket key]
                        if dij != 0:        
                            bra_cre, bra_annih = get_amplitude(i_tmp)
                            ket_cre, ket_annih = get_amplitude(j_tmp)
                            #print bra_cre, bra_annih, ket_cre, ket_annih
#                            print "D[%d][%d], Amplitudes: t[%s][%s] --> t[%s][%s], dij = %d" % (p, q, tuple(bra_cre), tuple(bra_annih), tuple(ket_cre), tuple(ket_annih), dij)
                            #print "D[%d][%d], " % (p, q)

                    #print "D[%d][%d], Contribution from ON %s, to ON %s, dij = %s" % (p, q, i_tmp, j_tmp, dij)
                    #print "  %d" % (dij)
                    Dpq += abs(dij)

            D[p][q] = Dpq

    for i in range(len(D)):
        print D[i]

    # Plot 1RDM as heatmap
#    cmap = plt.get_cmap('coolwarm')
#    levels = MaxNLocator(nbins=500, integer=False, symmetric=False, prune=None).bin_boundaries(D.min(), D.max())
#    x, y = np.arange(Nbasis), np.arange(Nbasis)
#    x1, y1 = np.arange(Nbasis+1), np.arange(Nbasis+1)
#    #plt.contourf(x, y, D, cmap=cmap, levels=levels)
#    plt.pcolor(x1, y1, D, cmap=cmap, vmin=D.min(), vmax=D.max())
#    plt.colorbar()
#    plt.show()
