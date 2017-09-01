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

def plot_heatmap(x, y, D):

    cmap = plt.get_cmap('coolwarm')
    plt.pcolor(x, y, D, cmap=cmap, vmin=D.min(), vmax=D.max())
    plt.colorbar()
    plt.show()

if __name__ == "__main__":

    values = parse_heatmap(fn_heat, dl)
    print values
    x, y = np.arange(dim+1), np.arange(dim+1)
    plot_heatmap(x, y, values)
