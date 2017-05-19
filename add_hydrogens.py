#!/usr/bin/python

import sys
import numpy as np

if len(sys.argv) != 6:
    print "Usage: add_hydrogens.py bare-structure middle-atom-index bond-length existing-element new-element"
    print " Note: Use python indexing"
    exit(0)


fn_in = sys.argv[1]
idx = int(sys.argv[2])
BL = float(sys.argv[3])
elem = str(sys.argv[4])
new_elem = str(sys.argv[5])

def parse_xyz(fn_in):

    sym = []
    x = []
    y = []
    z = []
    with open(fn_in, 'r') as f:
        lines = f.readlines()
        for line in lines:
            tokens = line.split()
            if len(tokens) != 4:
                continue
            else:
                sym.append(tokens[0])
                x.append(float(tokens[1]))
                y.append(float(tokens[2]))
                z.append(float(tokens[3]))
    Natoms = len(sym)

    return Natoms, sym, x, y, z

def distance(mid_Se, edge_Se):

    dist = np.sqrt((mid_Se[0]-edge_Se[0])**2 + (mid_Se[1]-edge_Se[1])**2 + (mid_Se[2]-edge_Se[2])**2)
    return dist

if __name__ == "__main__":

    Natoms, sym, x, y, z = parse_xyz(fn_in)
    
    mid_Se = np.array([x[idx], y[idx], z[idx]])
    for i in range(Natoms):
        if sym[i] == elem:
            edge_Se = np.array([x[i], y[i], z[i]])
            dist = distance(mid_Se, edge_Se)
            if dist == 0.0:
                continue
            else:
                scale = (dist + BL) / dist
                x_new = mid_Se[0] + scale*(edge_Se[0] - mid_Se[0])
                y_new = mid_Se[1] + scale*(edge_Se[1] - mid_Se[1])
                z_new = mid_Se[2] + scale*(edge_Se[2] - mid_Se[2])
                sym.append(new_elem)
                x.append(x_new)
                y.append(y_new)
                z.append(z_new)
        else:
            continue

    fn_out = fn_in.strip()[:-4] + "_hyd.xyz"
    with open(fn_out, 'w') as f:
        f.write("%d\n\n" % (len(sym)))
        for i in range(len(sym)):
            atom = sym[i]
            x_new = x[i]
            y_new = y[i]
            z_new = z[i]
            f.write("%s     %12.10f     %12.10f     %12.10f\n" % (atom, x_new, y_new, z_new))
