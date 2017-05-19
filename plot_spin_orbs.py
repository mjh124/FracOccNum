#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) != 2:
    print "Usage: plot_spin_orbs.py gpaw-output"
    print "Warning: this script does not work for systems with more than 1000 orbitals"
    exit(0)

fn_out = sys.argv[1]

def parse_ef(gpaw_out):

    fermi = []
    with open(gpaw_out, 'r') as f:
        lines = f.readlines()
        for line in lines:
           if "Fermi Level:" in line:
               fermi.append(float(line.split()[2]))
    return fermi[-1]

def parse_en_levels(gpaw_out):

    spin_up = []
    spin_down = []
    with open(gpaw_out, 'r') as f:
        lines = f.readlines()
        Nlines = len(lines)
        for line in range(Nlines):
            if "Eigenvalues" in lines[line]:
                start = int(line)
        for i in range(start+1, start+1000):
            line = lines[i]
            tokens = line.split()
            if len(tokens) != 5:
                break
            spin_up.append(float(tokens[1]))
            spin_down.append(float(tokens[3]))
    return spin_up, spin_down

def plot_levels(spin_up, spin_down, ef):

    x_up = np.ones(len(spin_up))
    x_down = np.zeros(len(spin_down))
    y_up = []
    y_down = []
    for i in range(len(spin_up)):
        y_up.append(spin_up[i]-ef)
        y_down.append(spin_down[i]-ef)
    plt.scatter(x_up, y_up, c='k', marker="_")
    plt.scatter(x_down, y_down, c='k', marker="_")
    plt.show()

#############################################

if __name__ == "__main__":

    ef = parse_ef(fn_out)
    spin_up, spin_down = parse_en_levels(fn_out)
    plot_levels(spin_up, spin_down, ef)
