#!/usr/bin/python

import sys
import numpy as np

if len(sys.argv) != 4:
    print "Usage: RadCutoff.py xyz-file rad-cutoff index"
    print " Indexing is in normal counting, coverted to python"
    exit(0)

fn_xyz = sys.argv[1]
cut = float(sys.argv[2])
idx = int(sys.argv[3])

def parse_XYZ(fn_xyz):

    sym = []
    x = []
    y = []
    z = []
    with open(fn_xyz, 'r') as f:
        Natoms = int(f.readline())
        lines = f.readlines()[1:]
        for line in lines:
            tokens = line.split()
            sym.append(tokens[0])
            x.append(float(tokens[1]))
            y.append(float(tokens[2]))
            z.append(float(tokens[3]))
    return Natoms, sym, x, y, z

def Rad_Cutoff(Natoms, x, y, z, cut, idx):

    trunc_pydx = []
    for i in range(Natoms):
        dist = np.sqrt((x[i]-x[pydx])**2 + (y[i]-y[pydx])**2 + (z[i]-z[pydx])**2)
        if dist < cut:
            trunc_pydx.append(i)
    return trunc_pydx

if __name__ == "__main__":

    pydx = idx-1
    Natoms, sym, x, y, z = parse_XYZ(fn_xyz)
    trunc_pydx = Rad_Cutoff(Natoms, x, y, z, cut, pydx)

    fn_out = fn_xyz.strip()[:-4] + "_atom" + str(idx) + "_"  + str(cut) + "A.xyz"
    with open(fn_out, 'w') as f:
        f.write("%d\n\n" % (len(trunc_pydx)))
        for i in trunc_pydx:
            symbol = sym[i]
            x_coord = x[i]
            y_coord = y[i]
            z_coord = z[i]
            f.write("%s    %12.6f    %12.6f    %12.6f\n" % (symbol, x_coord, y_coord, z_coord))
                
