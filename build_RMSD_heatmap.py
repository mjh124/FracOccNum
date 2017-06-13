#!/usr/bin/python

import sys
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

if len(sys.argv) != 2:
    print "Usage: build_RMSD_heatmap.py BL"
    exit(0)

BL = str(sys.argv[1])

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

if __name__ == "__main__":
 
    #Temps1, Temps2 = np.arange(0, 40001, 5000), np.arange(0, 40001, 5000)
    Temps1, Temps2 = np.arange(0, 50001, 5000), np.arange(0, 50001, 5000)

    RMSDs = np.zeros((len(Temps1), len(Temps2)))
    Ens = np.zeros((len(Temps1), len(Temps2)))
    for i in range(len(Temps1)):
        #fn1 = 'N2_' + str(BL) + 'A_' + str(Temps1[i]) + 'K_CISDDens.cube'
        #print 'reading', fn1
        fn_en1 = 'N2_' + str(BL) + 'A_' + str(Temps1[i]) + 'K.out'
        en1 = extract_CISDenergy(fn_en1)
        #dens1 = parse_cube(fn1)

        for j in range(len(Temps2)):
            #fn2 = 'N2_' + str(BL) + 'A_' + str(Temps2[j]) + 'K_CISDDens.cube'
            #print ' reading', fn2
            fn_en2 = 'N2_' + str(BL) + 'A_' + str(Temps2[j]) + 'K.out'
            en2 = extract_CISDenergy(fn_en2)
            #dens2 = parse_cube(fn2)
            #diff_dens, rmsd_of_diff = difference_density(dens1, dens2)
            #RMSDs[i][j] = rmsd_of_diff
            #print i, j, rmsd_of_diff
            en_diff = en1 - en2
            Ens[i][j] = en_diff

#    # Slices
    y0 = Ens[0][:]
#    y5000 = RMSDs[1][:]
#    y10000 = RMSDs[2][:]
#    y15000 = RMSDs[3][:]
    y20000 = Ens[4][:]
#    y25000 = RMSDs[5][:]
#    y30000 = RMSDs[6][:]
#    y35000 = Ens[7][:]
    y40000 = Ens[8][:]
#    y45000 = RMSDs[9][:]
#    y50000 = RMSDs[10][:]
#
#    # Plot slices
    plt.plot(Temps1, y0, '-o', label='0K')
    plt.plot(Temps1, y20000, '-o', label='20000K')
    plt.plot(Temps1, y40000, '-o', label='40000K')
    plt.legend(loc='lower left')
    plt.show()

    # Plot 1RDM as heatmap
#    cmap = plt.get_cmap('coolwarm')
#    #plt.pcolor(Temps1, Temps2, RMSDs, cmap=cmap, vmin=RMSDs.min(), vmax=RMSDs.max())
#    plt.pcolor(Temps1, Temps2, Ens, cmap=cmap, vmin=Ens.min(), vmax=Ens.max())
#    plt.colorbar()
#    plt.show()
