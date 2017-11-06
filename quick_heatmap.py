#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) != 4:
    print "Usage: quick_heatmap.py heatmap-file #deadlines dimension-of-axes"
    print " Format of heatmap-file: x, y, value"
    exit(0)

fn_heat = sys.argv[1]
dl = int(sys.argv[2])
dim = int(sys.argv[3])

def parse_heatmap(fn_heat, dl):

    val = np.zeros((dim, dim))
    with open(fn_heat, 'r') as f:
        lines = f.readlines()[dl:]
        for line in lines:
            x_idx = int(line.split()[0])
            y_idx = int(line.split()[1])
            val[x_idx][y_idx] = float(line.split()[2])
    return val

def make_HF_OccMat(Nocc, Nvirt):

    Ntot = Nocc + Nvirt
    vals = np.zeros((Ntot, Ntot))
    for i in range(Nocc):
        vals[i][i] = 1
    return vals

def make_FONHF_OccMat(Nocc, Nvirt, MO_ens, T):

    Ntot = Nocc + Nvirt
    vals = np.zeros((Ntot, Ntot))
    for i in range(Ntot):
        ni = 1 / (1 + np.exp((MO_ens[i])/T))
        vals[i][i] = ni
    return vals

def plot_heatmap(x, y, D):

    cmap = plt.get_cmap('Blues')
    #cmap = plt.get_cmap('coolwarm')
    plt.axis([x.min(), x.max(), y.min(), y.max()])
    plt.pcolor(x, y, D, cmap=cmap, vmin=D.min(), vmax=D.max())
    plt.colorbar()
    plt.show()

def normalize_values(vals, biggest):

    for i in range(len(vals)):
        for j in range(len(vals)):
            vals[i][j] /= biggest
    return vals

if __name__ == "__main__":

    values = parse_heatmap(fn_heat, dl)
#    biggest = np.max(values)
#    print biggest
#    norm_values = normalize_values(values, biggest)
    #print values
#    print len(norm_values)
#    plot_heatmap(x, y, norm_values)
    x, y = np.arange(dim+1), np.arange(dim+1)
    plot_heatmap(x, y, values)

#    Nocc = 8
#    Nvirt = 16
#    x, y = np.arange(24), np.arange(24)
#    #x, y = np.arange(Nocc+Nvirt), np.arange(Nocc+Nvirt)
#    HF = make_HF_OccMat(Nocc, Nvirt)
#    plot_heatmap(x, y, HF)
#
#    T = 1
#    MO_ens = [-15, -15, -10, -8, -5, -1, -0.5, -0.1, 0.1, 0.1, 0.25, 0.4, 0.6, 1.0, 1.2, 1.8, 2.5, 10, 10, 10, 10, 10, 10, 10]
#    FONHF = make_FONHF_OccMat(Nocc, Nvirt, MO_ens, T)
#    #plot_heatmap(x, y, FONHF)
