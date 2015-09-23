#!/usr/bin/env python

import sys
import Ef_opt_mod

if len(sys.argv) != 5:
    print "Usage: test.py fMO alpha-elec beta-elec temp"
    exit(0)

fMO = sys.argv[1]
Nelec_alpha = int(sys.argv[2])
Nelec_beta = int(sys.argv[3])
T = int(sys.argv[4])

if __name__ == "__main__":

    Ef_a, Ef_b = Ef_opt_mod.execute(fMO, Nelec_alpha, Nelec_beta, T)
    print "Alpha occupations =",Ef_a 
    print "Beta occupations =",Ef_b
