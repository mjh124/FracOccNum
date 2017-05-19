#!/usr/bin/python

import sys
import numpy as np
from scipy.sparse import csr_matrix
#from scipy.sparse.csr_matrix import transpose, multiply
from scipy.sparse.linalg import inv
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

if len(sys.argv) != 4:
    print "Usage: CISDcoeff_parser.py qchem-output Nocc Nvirt"
    exit(0)

fn_qchem = sys.argv[1]
Nocc = int(sys.argv[2])
Nvirt = int(sys.argv[3])

def get_Hdiag(fn_qchem):

    message = "Total energy ="
    states = []
    with open(fn_qchem, 'r') as f:
        for line in f:
            if message in line:
                states.append(float(line.split()[3]))
    Hdiag = np.zeros((len(states), len(states)))
    for i in range(len(states)):
        Hdiag[i][i] = states[i]
    return Hdiag

def parse_singles(fn_qchem, message):

    singles = []
    f = open(fn_qchem, 'r')
    for line in f:
        if message in line:
            for line in f:
                tokens = line.split()
                if len(tokens) == 5:
                    break
                for i in tokens:
                    singles.append(float(i))
    f.close()
    return singles

def parse_doubles(fn_qchem, message):

    doubles = []
    f = open(fn_qchem, 'r')
    for line in f:
        if message in line:
            for line in f:
                tokens = line.split()
                if len(tokens) == 0 or tokens[0] == 'Amplitude':
                    break
                for i in tokens:
                    doubles.append(float(i))
    f.close()
    return doubles

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

def multiply_matrices(A, B):

    C = np.zeros((A.shape[0], B.shape[1]))
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                C[i][j] += A[i][k] * B[k][j]
    return C

def contract_MatandVec(Mat_A, Vec_B):

    C = np.zeros((Mat_A.shape[0], 1))
    for i in range(len(Mat_A)):
        for k in range(len(Mat_A)):
            C[i] += Mat_A[i][k] * Vec_B[k]
    return C

def write_Mat2File(matrix, Nroots):

    fn_out = "Hdet_" + str(Nroots) + "roots.txt"
    x, y = matrix.shape
    with open(fn_out, 'w') as fout:
        for i in range(x):
            for j in range(y):
#                if matrix[i][j] > 0.00000001:
                fout.write("%d  %d  %20.16f\n" % (i, j, matrix[i][j]))
#                else:
#                    continue

if __name__ == "__main__":

    Hdiag = get_Hdiag(fn_qchem)
    #print Hdiag
    Nroots, throw = Hdiag.shape

    Nsing = Nocc * Nvirt
    Ndoub = (Nocc * Nvirt)**2
    Namps = Nsing + Ndoub
    #print Nsing, Ndoub, Namps

    singles_message = '2 ' + str(Nocc) + ' ' + str(Nvirt)
    singles = parse_singles(fn_qchem, singles_message)
    print len(singles)

    doubles_message = '4 ' + str(Nocc) + ' ' + str(Nocc) + ' ' + str(Nvirt) + ' ' + str(Nvirt)
    doubles = parse_doubles(fn_qchem, doubles_message) # Did all excitations, rewrite to do a specific one at a time, then can construct the proper matrix afterwards
    print len(doubles)

#    Nstates = len(singles) / int(Nsing)
#    test = len(doubles) / int(Ndoub)
    #print Nstates, Namps
#    if Nstates != test:
#        exit("ERROR: Different number of singles and doubles amplitudes")

#    CI_AmpMat = Build_CI_Amplitude_Matrix(singles, doubles, Nstates, Namps)
#    print CI_AmpMat.shape

#    # Normalize CI coefficients
#    for i in range(Nroots):
#        CI_coeff = CI_AmpMat[i,:]
#        test = np.dot(CI_coeff, CI_coeff.T)
#        for j in range(len(CI_coeff)):
#            CI_coeff[j] /= np.sqrt(test)

#    CI_Amp_spar = csr_matrix(CI_AmpMat)
#    print CI_Amp_spar
    #CI_Amp_sparT = CI_Amp_spar.transpose()

    # Overlap Matrix
    #S = np.dot(CI_AmpMat, CI_AmpMat.T)
#    S = np.dot(CI_AmpMat.T, CI_AmpMat)
    #S_inv = np.linalg.inv(S)
    #for i in range(4692):
    #    for j in range(4692):
    #        if S[i][j] <= 1e-6:
    #            S[i][j] = 0

    # Store S as sparse matrix
#    S_spar = csc_matrix(S)
#    S_spar_inv = inv(S_spar)

#    zeros = 0
#    for i in range(4692):
#        for j in range(4692):
#            if S[i][j] <= 1e-6:
#                zeros += 1
#    print float(zeros) / 4692**2

    #print 'determinant =',np.linalg.det(S)
    #print ' ',S_inv.shape
    #print ' ',S_spar.shape

    # Do matrix multiplication (H_det = C * H_diag * C^T)
#    CI_tmp = np.dot(Hdiag, CI_AmpMat)
#    H_det = np.dot(CI_AmpMat.T, CI_tmp)
#    print CI_tmp.shape
#    print H_det.shape
    #write_Mat2File(H_det, Nroots)

    # <H> = E_1 = C_1^T * H_det * C_1
#    SC = np.dot(S_inv, CI_AmpMat)
#    En = []
#    for i in range(Nroots):
#        CI_coeff = SC[i,:]
#        intermediate = np.dot(H_det, CI_coeff)
#        energy = np.dot(CI_coeff.T, intermediate)
#        En.append(energy)
        #print "Root #", i+1, "  Root Energy =", energy

    # <H^2> = C_1^T * H_det * H_det * C_1
#    SC = np.dot(S_inv, CI_AmpMat)
#    Hdet_sq = np.dot(H_det, H_det)
#    #SinvHdet = np.dot(S_inv, H_det)
#    #HdetSinvHdet = np.dot(H_det, SinvHdet)
#    En_sq = []
#    for i in range(Nroots):
#        CI_coeff = SC[i,:]
#        #intermediate = np.dot(HdetSinvHdet, CI_coeff)
#        intermediate = np.dot(Hdet_sq, CI_coeff)
#        energy_sq = np.dot(CI_coeff.T, intermediate)
#        En_sq.append(energy_sq)
#        #print "Root #", i+1, "  Root Energy Squared", energy_sq

    # Calculate variance in energy: <H^2> - <H>^2
#    for i in range(Nroots):
#        variance = En_sq[i] - En[i]**2
#        print "Root # ",i+1, "variance = ", variance

    # To do:
    #   How many roots do we need to get convergence (use RMSD to quantify)
    #   Do optimization w.r.t energy variance instead of energy
