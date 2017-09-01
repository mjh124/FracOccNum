#!/usr/bin/python

import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

if len(sys.argv) != 3:
    print "Usage: build_RMSD_heatmap.py BL En-or-RMSD"
    exit(0)

BL = str(sys.argv[1])
prop = str(sys.argv[2])

def parse_cube(fn):

    density = []
    with open(fn, 'r') as f:
        lines = f.readlines()[8:]
        for line in lines:
            tokens = line.split()
            for i in tokens:
                density.append(float(i))
    return density

def extract_CISDenergy(filename):

    message = "Total energy ="
    states = []
    with open(filename, 'r') as f:
        for line in f:
            if message in line:
                states.append(float(line.split()[3]))
    if len(states) == 0:
        energy = 1e5
    else:
        energy = states[0]
    return energy

def calc_RMSD(dens1, dens2):

    rmsd_ker = 0.0
    for i in range(len(dens1)):
        rmsd_ker += (dens1[i] - dens2[i])**2
    rmsd_ker /= len(dens1)
    rmsd = np.sqrt(rmsd_ker)
    return rmsd

def difference_density(dens1, dens2):

    diff = np.zeros(len(dens1))
    diff_per = np.zeros(len(dens1))
    max_diff = 0.0
    for i in range(len(dens1)):
        diff[i] = dens1[i] - dens2[i]
        diff_per[i] = 100 * ((dens1[i] - dens2[i]) / dens1[i])
        if abs(diff_per[i]) > max_diff:
            max_diff = diff_per[i]
    #print max_diff

    diff_rmsd = 0.0
    for i in range(len(diff_per)):
        diff_rmsd += diff_per[i]**2
    rmsd_of_diff = np.sqrt(diff_rmsd / len(diff_per))

    return diff, rmsd_of_diff

def plot_heatmap(x, y, heat):

    cmap = plt.get_cmap('coolwarm')
    plt.pcolor(x, y, heat, cmap=cmap, vmin=heat.min(), vmax=heat.max())
    plt.colorbar()
    plt.show()

if __name__ == "__main__":
 
    Temps1, Temps2 = np.arange(0, 45001, 5000), np.arange(0, 45001, 5000)
    #Temps1, Temps2 = np.arange(0, 50001, 5000), np.arange(0, 50001, 5000)

    RMSDs = np.zeros((len(Temps1), len(Temps2)))
    Ens = np.zeros((len(Temps1), len(Temps2)))
    if prop == 'RMSD':
        for i in range(len(Temps1)):
            fn1 = 'N2_' + str(BL) + 'A_' + str(Temps1[i]) + 'K_CISDDens.cube'
            print 'reading', fn1
            dens1 = parse_cube(fn1)
            for j in range(len(Temps2)):
                fn2 = 'N2_' + str(BL) + 'A_' + str(Temps2[j]) + 'K_CISDDens.cube'
                dens2 = parse_cube(fn2)
                diff_dens, rmsd_of_diff = difference_density(dens1, dens2)
                RMSDs[i][j] = calc_RMSD(dens1, dens2)
        plot_heatmap(Temps1, Temps2, RMSDs)

    elif prop == 'En':
        for i in range(len(Temps1)):
            fn1 = 'N2_' + str(BL) + 'A_' + str(Temps1[i]) + 'K.out'
            print 'reading', fn1
            en1 = extract_CISDenergy(fn1)
            for j in range(len(Temps2)):
                fn2 = 'N2_' + str(BL) + 'A_' + str(Temps2[j]) + 'K.out'
                en2 = extract_CISDenergy(fn2)
                Ens[i][j] = en1 - en2
        plot_heatmap(Temps1, Temps2, Ens)

    else:
        exit('ERROR: Option not implemented')
