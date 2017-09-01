#!/usr/bin/python

import sys
import copy
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

if len(sys.argv) != 4:
    print "Usage: CISD_1RDM_fromQchem.py Nocc Nvirt fn-qchem"
    print "    Nocc = #a_occ + #b_occ"
    print "    Nvirt = #a_virt + #b_virt"
    print "    Orbital ordering --> a_occ, b_occ, a_virt, b_virt"
    
    exit(0)

Nocc = int(sys.argv[1])
Nvirt = int(sys.argv[2])
fn_qchem = sys.argv[3]

def parse_singles(fn_qchem, message):

    count = 0
    Amps_sing = []
    f = open(fn_qchem, 'r')
    for line in f:
        if message in line and count == 0:
            for line in f:
                tokens = line.split()
                if len(tokens) == 5:
                    count += 1
                    break
                for i in tokens:
                    Amps_sing.append(float(i))
    f.close()
    return Amps_sing

def parse_doubles(fn_qchem, message):

    count = 0
    Amps_doub = []
    f = open(fn_qchem, 'r')
    for line in f:
        if message in line and count == 0:
            for line in f:
                tokens = line.split()
                if len(tokens) == 0 or tokens[0] == 'Amplitude':
                    count =+ 1
                    break
                for i in tokens:
                    Amps_doub.append(float(i))
    f.close()
    return Amps_doub

def get_SinglesCIcoeff_index(ON_string, Nocc, Nvirt):

    ON = list(ON_string)
    occ = ON[:Nocc]
    virt = ON[Nocc:]

    occ_idx = []
    for i in range(len(occ)):
        if float(occ[i]) == 0:
            occ_idx.append(i)
    virt_idx = []
    for i in range(len(virt)):
        if float(virt[i]) == 1:
            virt_idx.append(i)

    print occ_idx, virt_idx

    index = -10
    if len(occ_idx) == 1:
        index = occ_idx[0]*Nvirt+virt_idx[0]
    else:
        exit("ERROR: Excitation Level Not Implemented")

    return index

def get_DoublesCIcoeff_index(ON_string, Nocc, Nvirt):

    ON = list(ON_string)
    occ = ON[:Nocc]
    virt = ON[Nocc:]

    occ_idx = []
    for i in range(len(occ)):
        if float(occ[i]) == 0:
            occ_idx.append(i)
    virt_idx = []
    for i in range(len(virt)):
        if float(virt[i]) == 1:
            virt_idx.append(i)

    #The order of operation matters, same final strings can have multiple indices
    index = -10
    if len(occ_idx) == 2 and len(virt_idx) == 2:
        index = occ_idx[0]*Nocc*Nvirt*Nvirt + occ_idx[1]*Nvirt*Nvirt + virt_idx[0]*Nvirt + virt_idx[1]

    return index

def form_HF_string(Nocc, Nvirt):

    ON_hf = ''
    for i in range(Nocc):
        ON_hf += '1'
    for i in range(Nvirt):
        ON_hf += '0'
    return ON_hf

def do_excitation(ON, chi):

    ON_array = list(ON)
    ON_array[chi[0]] = '0'
    ON_array[chi[1]] = '1'
    ON_ex = "".join(ON_array)
    return ON_ex

def form_single_ONStrings(ON, Nocc, Nvirt):

    singles = []
    for i in range(Nocc):
        for j in range(Nocc, Nocc+Nvirt):
            chi = [i, j]
            ON_ex = do_excitation(ON, chi)
            singles.append(ON_ex)
    return singles

def form_double_ONStrings(ON, Nocc, Nvirt):

    doubles = []
#    Key2Degen = {}
    for i in range(Nocc):
        for j in range(Nocc, Nocc+Nvirt):
            chi1 = [i, j]
            ON_cp = copy.deepcopy(ON)
            ON_ex1 = do_excitation(ON_cp, chi1)
            for n in range(Nocc):
                for m in range(Nocc, Nocc+Nvirt):
                    chi2 = [n, m]
                    ON_ex2 = do_excitation(ON_ex1, chi2)
                    doub_idx = get_DoublesCIcoeff_index(ON_ex2, Nocc, Nvirt)
                    if ON_ex2 not in doubles and doub_idx > 0:
                        doubles.append(ON_ex2)
#                        Key2Degen[ON_ex2] = 1
#                    elif ON_ex2 in doubles and doub_idx > 0:
#                        Key2Degen[ON_ex2] = Key2Degen.get(ON_ex2) + 1
                    else:
                        continue
                    #print chi1, chi2, ON_ex2
    return doubles#, Key2Degen

def get_amplitude(vec):

    annih = []
    create = []
    ON = form_HF_string(Nocc, Nvirt)
    Nbasis = Nocc + Nvirt
    for i in range(Nbasis):
        ON_HF = list(ON)
        vec_diff = int(ON_HF[i]) - int(vec[i])
        if vec_diff == 1:
            annih.append(i)
        elif vec_diff == -1:
            create.append(i)
    return annih, create

def form_stringArray_pairs(ONstrings):

    ON_tuple = []
    for i in range(len(ONstrings)):
        ON = ONstrings[i] 
        ON_int = [int(ON[j]) for j in range(len(ON))]
        ON_tuple.append((ON, ON_int))
    return ON_tuple

def Build_CI_Amplitude_Matrix(singles, doubles, Nstates, Namps):

    s = np.reshape(np.asarray(singles), (Nstates, Nsing))
    d = np.reshape(np.asarray(doubles), (Nstates, Ndoub))
    CI_AmpMat = np.zeros((Nstates,Namps))
    for i in range(Nstates):
        for j in range(Nsing):
            CI_AmpMat[i][j] = s[i][j]
    for i in range(Nstates):
        for j in range(Nsing, Namps):
            b = j - Nsing
            CI_AmpMat[i][j] = d[i][b]
    return CI_AmpMat

def write_density(D, Nbasis):

    fn_dens = fn_qchem.strip()[:-4] + '_density.txt'
    print "writing density file, ",fn_dens
    with open(fn_dens, 'w') as f:
        f.write("# x_idx y_idx Density\n")
        for i in range(Nbasis):
            for j in range(Nbasis):
                f.write("%d    %d    %.8e\n" % (i, j, D[i][j]))

def plot_heatmap(x, y, D):

    cmap = plt.get_cmap('coolwarm')
    plt.pcolor(x1, y1, D, cmap=cmap, vmin=D.min(), vmax=D.max())
    plt.colorbar()
    plt.show()

if __name__ == "__main__":

    # Generate ON strings for each excitation level
    ON = form_HF_string(Nocc, Nvirt)
    ON_hf = []
    ON_hf.append(ON)
    singles = form_single_ONStrings(ON, Nocc, Nvirt)
    doubles = form_double_ONStrings(ON, Nocc, Nvirt)
#    doubles, Key2Degen = form_double_ONStrings(ON, Nocc, Nvirt)
    print len(singles), len(doubles)
#    for i in Key2Degen:
#        print i, Key2Degen[i]

    # Build Qchem parsing messages
    message_sing = '2 ' + str(Nocc) + ' ' + str(Nvirt)
    Amps_sing = parse_singles(fn_qchem, message_sing)
    message_doub = '4 ' + str(Nocc) + ' ' + str(Nocc) + ' ' + str(Nvirt) + ' ' + str(Nvirt)
    Amps_doub = parse_doubles(fn_qchem, message_doub)
    print len(Amps_sing), len(Amps_doub)

    #Make overall bra and ket and build string/array pairs, could ultimately control excitation level here
    bra = ON_hf + singles + doubles
    ket = ON_hf + singles + doubles
    bra_pairs = form_stringArray_pairs(bra)
    ket_pairs = form_stringArray_pairs(ket)

    #Some excitations result in same string, do I need to keep track of degeneracy of some strings?
    ONstring2Amp = {}
    ONstring2Amp[ON] = 1.0 #What should HF amplitude be?
    for i in range(len(singles)):
        ONstring2Amp[singles[i]] = Amps_sing[i]
    for i in range(len(doubles)):
        d_idx = get_DoublesCIcoeff_index(doubles[i], Nocc, Nvirt)
        ONstring2Amp[doubles[i]] = Amps_doub[d_idx]
    #for i in ONstring2Amp:
    #    print i, ONstring2Amp[i]

    Thres1 = 1e-5
    Thres2 = 1e-8

    sigBraPairs = []
    for i in range(len(bra_pairs)):
        i_key = bra_pairs[i][0]
        if abs(ONstring2Amp[i_key]) >= Thres1:
            sigBraPairs.append(bra_pairs[i])
    print("Finding significant Bra strings: %.3f %% reduction" % (100.0 - 100.0*len(sigBraPairs)/len(bra_pairs)) )
    sigKetPairs = []
    for i in range(len(ket_pairs)):
        i_key = ket_pairs[i][0]
        if abs(ONstring2Amp[i_key]) >= Thres1:
            sigKetPairs.append(ket_pairs[i])
    print("Finding significant Ket strings: %.3f %% reduction" % (100.0 - 100.0*len(sigKetPairs)/len(ket_pairs)) )

    Nbasis = Nocc + Nvirt
    D = np.zeros((Nbasis, Nbasis))
    for p in range(Nbasis):
        for q in range(Nbasis):
            print 'Writing idx ', p, q
            # form the matrix elements, Dpq = <psi|a+_pa_q|psi>
            Dpq = 0

            for i in sigBraPairs:
                i_key = i[0]
                i_amp = ONstring2Amp[i_key]
                i_array = i[1]

                for j in sigKetPairs:

                    if ONstring2Amp[j[0]]*i_amp <= Thres2:
                        continue

                    j_key = j[0]
                    j_array = j[1] 

                    if j_array[q] == 1:

                        #Perform excitation, first remove an electron from q then add one to p
                        gamma_q = 1
                        for k in range(0, q):
                            gamma_q *= (-1)**(j_array[k])

                        #delta_q = 1 #Condition above ensures this
                        j_array[q] = 0 #Annihilation to the right

                        gamma_p = 1
			for k in range(0, p):
                            gamma_p *= (-1)**(j_array[k])

#                        if j_array[p] == 0: 
#                            j_array[p] = 1 #Creation to the right
#                        else:
#                            continue
                        delta_p = 0
                        if j_array[p] == 0:
                            delta_p = 1
                            j_array[p] = 1

                        #Make sure overlap between ON vectors <Ki|Kj_qp> = 1
                        #if i_key == j_key:
                        if np.array_equal(i_array, j_array):

                            #Bring everything together
                            #Dpq += gamma_p * gamma_q * i_amp * ONstring2Amp[j_key]
                            Dpq += delta_p * gamma_p * gamma_q * i_amp * ONstring2Amp[j_key]
                            #Dpq += Key2Degen[j_key] * gamma_p * gamma_q * i_amp * ONstring2Amp[j_key]
                            #Dpq += dij

                        #Reset j so we don't need to make deepcopy
                        j_array[q] = 1
                        if delta_p == 1 and p != q:
                            j_array[p] = 0
#                        if p != q:
#                            j_array[p] = 0

                    #print "  %d" % (dij)
                    #Dpq += abs(dij)

            D[p][q] = Dpq

    write_density(D, Nbasis)

    #x1, y1 = np.arange(Nbasis+1), np.arange(Nbasis+1)
    #plot_heatmap(x1, y1, D)
