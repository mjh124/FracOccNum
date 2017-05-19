#!/usr/bin/python

import sys
import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

if len(sys.argv) != 5:
    print "Usage: plot_force_vectors.py file-forces file-xyz slice-number number-atoms"
    exit(0)

fn_force = sys.argv[1]
fn_xyz = sys.argv[2]
Nslice = int(sys.argv[3])
Natoms = int(sys.argv[4])

def parse_file(filename):

    x = []
    y = []
    z = []
    readto = Natoms+2
    with open(filename, 'r') as f:
        lines = f.readlines()[:readto]
        for line in lines:
            tokens = line.split()
            if tokens[0] == 'Au':
                x.append(float(tokens[1]))
                y.append(float(tokens[2]))
                z.append(float(tokens[3]))
    return x, y, z

if __name__ == "__main__":

    x_force, y_force, z_force = parse_file(fn_force)
    x_coord, y_coord, z_coord = parse_file(fn_xyz)

    for i in range(len(x_coord)):
        print x_coord[i], x_force[i]

    fig = plt.figure()
    x, y, z = np.meshgrid(np.arange(7.0, 18.0, 0.2),
                      np.arange(7.0, 18.0, 0.2),
                      np.arange(6.0, 19.0, 0.2))
    plt.quiver(x_coord, y_coord, x_force, y_force)
    plt.show()
