#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) != 5:
    print "Usage: parse_CISDEn_2Dgrid.py prefix temp-min temp-max temp-step"
    exit(0)

prefix = sys.argv[1]
t_min = int(sys.argv[2])
t_max = int(sys.argv[3])
t_step = int(sys.argv[4])

def extract_CISDenergy(filename):

    message = "Total energy ="
    states = []
    with open(filename, 'r') as f:
        for line in f:
            if message in line:
                states.append(float(line.split()[3]))
    if len(states) == 0:
        energy = -108.76
    else:
        energy = states[0]
    return energy

def extract_SpinSquared(filename):

    message = "<S^2> ="
    sSq = -0.1
    with open(filename, 'r') as f:
        for line in f:
            if message in line:
                sSq = float(line.split()[2])
    return sSq

def write_output(temps, energies, sSqs):

    fn_out = prefix + 'EnandsSq_forHeatmap.txt'
    with open(fn_out, 'w') as f:
        f.write("#Alpha-T  Beta-T  CISD-En  S^2\n")
        for i in range(len(temps)):
            for j in range(len(temps)):
                idx = i * len(temps) + j
                f.write("%d  %d  %10.8f  %6.4f\n" % (temps[i], temps[j], energies[idx], sSqs[idx]))

def plot_heatmap(x, y, D):

    cmap = plt.get_cmap('coolwarm')
    #plt.axis([x.min(), x.max(), y.min(), y.max()])
    plt.xticks(np.arange(min(x), max(x)+1, 20000))
    plt.yticks(np.arange(min(y), max(y)+1, 20000))
    plt.pcolor(x, y, D, cmap=cmap, vmin=D.min(), vmax=D.max())
    plt.colorbar()
    plt.show()

if __name__ == "__main__":

    temps = np.arange(t_min, t_max+1, t_step)
    print temps

    energies = []
    sSqs = []
    for i in range(len(temps)):
        for j in range(len(temps)):
            filename = prefix + str(temps[i]) + 'K_' + str(temps[j]) + 'K.out'
            energy = extract_CISDenergy(filename)
            energies.append(energy)
            sSq = extract_SpinSquared(filename)
            sSqs.append(sSq)
            #print energy, sSq

    print np.min(energies)
    write_output(temps, energies, sSqs)
    #S = np.reshape(np.asarray(sSqs), (len(temps), len(temps)))
    #E = np.reshape(np.asarray(energies), (len(temps), len(temps)))
    #plot_heatmap(temps, temps, S)
    #plot_heatmap(temps, temps, E)
