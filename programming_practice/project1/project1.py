#!/usr/bin/python

import numpy as np

geom = "geom.dat"

def parse_geom_file(filename):
    charge = []
    x = []
    y = []
    z = []
    with open(filename, 'r') as f:
        Natoms = int(f.readline()[0])
        contents = f.readlines()[0:]
    for line in contents:
        tokens = line.split()
        charge.append(int(tokens[0]))
        x.append(float(tokens[1]))
        y.append(float(tokens[2]))
        z.append(float(tokens[3]))
    return Natoms, charge, x, y, z

def bond_lengths(Natoms, x, y, z):
    bl_mat = np.zeros((Natoms, Natoms))
    for i in range(Natoms):
        for j in range(Natoms):
            dist = np.sqrt((x[i]-x[j])**2 + (y[i]-y[j])**2 + (z[i]-z[j])**2)
            bl_mat[i, j] = dist
    return bl_mat

Natoms, charge, x, y, z = parse_geom_file(geom)
print "Natoms =",Natoms
for i in range(Natoms):
    print "Atoms #",i,":",charge[i], x[i], y[i], z[i]
bl_mat = bond_lengths(Natoms, x, y, z)
print bl_mat
