#!/usr/bin/python

import sys
import numpy as np

if len(sys.argv) != 4:
    print "Usage: density_rmsd.py fn1 fn2 fn_out"
    exit(0)

#fn1 = 'N2_' + str(sys.argv[1]) + 'A_' + str(sys.argv[2]) + 'K.cube'
#fn2 = 'N2_' + str(sys.argv[1]) + 'A_' + str(sys.argv[3]) + 'K.cube'

fn1 = sys.argv[1]
fn2 = sys.argv[2]
fn_out = sys.argv[3]

def extract_preamble(fn):

    with open(fn, 'r') as f:
        preamble = f.readlines()[:8]
    return preamble

def parse_cube(fn):

    density = []
    with open(fn, 'r') as f:
        lines = f.readlines()[8:]
        for line in lines:
            tokens = line.split()
            for i in tokens:
                density.append(float(i))
    return density

def difference_density(dens1, dens2):

    diff = np.zeros(len(dens1))
    diff_per = np.zeros(len(dens1))
    max_diff = 0.0
    for i in range(len(dens1)):
        diff[i] = np.abs(dens1[i]) - np.abs(dens2[i])
        #diff[i] = dens1[i] - dens2[i]
        diff_per[i] = (dens1[i] - dens2[i]) / dens1[i]
        if abs(diff_per[i]) > max_diff:
            max_diff = diff_per[i]
    #print max_diff
    return diff, diff_per

def rmsd(dens1, dens2):

    rmsd_ker = 0.0
    for i in range(len(dens1)):
        rmsd_ker += (np.abs(dens1[i]) - np.abs(dens2[i]))**2
        #rmsd_ker += (dens1[i] - dens2[i])**2
    rmsd_ker /= len(dens1)
    rmsd = np.sqrt(rmsd_ker)
    return rmsd

def write_diffDens(preamble, diff_dens):

    #fn_out = 'N2_' + str(sys.argv[2]) + 'K_' + str(sys.argv[3]) + 'K_diffDens.cube'
    #fn_out = 'N2_tmp_diffDens.cube'
    with open(fn_out, 'w') as f:
        for i in range(len(preamble)):
            f.write("%s" % preamble[i])
        for i in range(len(diff_dens)):
            f.write("%.5e\n" % diff_dens[i])

if __name__ == "__main__":

    preamble = extract_preamble(fn1)

    dens1 = parse_cube(fn1)
    dens2 = parse_cube(fn2)

    diff_dens, diff_per = difference_density(dens1, dens2)
    diff_rmsd = 0.0
    for i in range(len(diff_per)):
        diff_rmsd += diff_per[i]**2
    rmsd = rmsd(dens1, dens2)
    print rmsd#, np.sqrt(diff_rmsd / len(diff_per))

    write_diffDens(preamble, diff_dens)
