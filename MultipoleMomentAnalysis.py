#!/usr/bin/python

import numpy as np
import sys

if len(sys.argv) != 2:
    print "Usage: QuadMom.py Cube-file"
    exit(0)

fn_cube = sys.argv[1]

def extract_preamble(fn_cube):

    preamble = []
    with open(fn_cube, 'r') as f:
        lines = f.readlines()[:8]
        for line in lines:
            preamble.append(line)
    return preamble

def extract_grid_parameters(preamble):

    Natoms = int(preamble[2].split()[0])
    Ngrid = []
    gp_spacing = []
    atoms = []
    for i in range(3):
        Ngrid.append(int(preamble[i+3].split()[0]))
        gp_spacing.append(float(preamble[i+3].split()[i+1]))
    for i in range(len(preamble)-1, len(preamble)-Natoms-1, -1):
        atoms.append(preamble[i])
    return Natoms, Ngrid, gp_spacing, atoms

def find_reference_position(atoms, Natoms):

    x = 0.0
    y = 0.0
    z = 0.0
    for i in range(Natoms):
        x += float(atoms[i].split()[2])
        y += float(atoms[i].split()[3])
        z += float(atoms[i].split()[4])
    ref_pos = np.array((x/Natoms, y/Natoms, z/Natoms))
    ref_pos /= BohrPerAng
    return ref_pos

def extract_density(fn_cube):

    dens = []
    with open(fn_cube, 'r') as f:
        lines = f.readlines()[8:]
        for line in lines:
            dens.append(float(line.split()[0]))
    return dens

def find_rl(ref_pos, gp, Ngrid, gp_spacing):

    x_gp = gp // (Ngrid[1]*Ngrid[2])
    y_gp = (gp // Ngrid[1]) % Ngrid[2]
    z_gp = gp % Ngrid[2]

    x_pos = x_gp * (gp_spacing[0] / BohrPerAng) - 1.0
    y_pos = y_gp * (gp_spacing[1] / BohrPerAng) - 1.0
    z_pos = z_gp * (gp_spacing[2] / BohrPerAng) - 1.0
    #print "%d %10.3f %10.3f %10.3f" % (gp, x_pos, y_pos, z_pos)

    rl = np.array((x_pos-ref_pos[0], y_pos-ref_pos[1], z_pos-ref_pos[2]))

    return rl

if __name__ == "__main__":

    BohrPerAng = 1.88973
    density = extract_density(fn_cube)
    preamble = extract_preamble(fn_cube)

    Natoms, Ngrid, gp_spacing, atoms = extract_grid_parameters(preamble)
    ref_pos = find_reference_position(atoms, Natoms)

#    for i in range(10000, 12000):
#        rl = find_rl(ref_pos, i, Ngrid, gp_spacing)
#        print rl

#    Qij = np.zeros((3,3))
#    for i in range(3):
#        for j in range(3):
#            qij = 0.0
#            for l in range(len(density)):
#                if i != j:
#                    rl = find_rl(ref_pos, l, Ngrid, gp_spacing)
#                    qij += density[l]*(3*rl[i]*rl[j])
#            Qij[i][j] = qij
#    print Qij

#    dip = np.zeros(3)
#    for i in range(3):
#        for l in range(len(density)):
#            rl = find_rl(ref_pos, l, Ngrid, gp_spacing)
#            print l, rl
#            dip[i] += density[l]*rl[i]
#    print dip

    total_dens = 0.0
    for i in density:
        total_dens += i
    print total_dens