#!/usr/bin/python

import sys
import numpy as np

if len(sys.argv) != 5:
    print 'Usage: test_idxSorter.py Nalpha Nbeta Nbasis Nfrozen'
    exit(0)

Na = int(sys.argv[1])
Nb = int(sys.argv[2])
Nbasis = int(sys.argv[3])
Nfroz = int(sys.argv[4])

def idx2MO(idx, Nalpha, Nbeta, Nbasis, Nfroz):                                                               
    NAvirt = Nbasis - (Nalpha + Nfroz)
    NBvirt = Nbasis - (Nbeta + Nfroz)
    if idx < Nalpha:
        MO_idx = idx + Nfroz
        print idx, 'alpha_occ', MO_idx
    elif idx >= Nalpha and idx < Nalpha+Nbeta:
        MO_idx = Nbasis + (idx-Nalpha) + Nfroz
        print idx, 'beta_occ', MO_idx
    elif idx >= Nalpha+Nbeta and idx < Nalpha+Nbeta+NAvirt:
        MO_idx = idx-Nbeta + Nfroz
        print idx, 'alpha_virt', MO_idx
    else: 
        MO_idx = idx + Nfroz + Nfroz
        print idx, 'beta_virt', MO_idx
    return MO_idx

if __name__ == '__main__':

    for i in range(2*(Nbasis-Nfroz)):
        MO_idx = idx2MO(i, Na, Nb, Nbasis, Nfroz)
