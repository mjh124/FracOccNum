#!/usr/bin/python

import sys
import numpy as np

if len(sys.argv) != 2:
    print "Usage qchem_test.py qtemplate"
    exit(0)

fn_qtemp = sys.argv[1]

def get_atom_positions(qtemplate, Natoms):

    fn_qchem = qtemplate
    coords = np.zeros((Natoms, 3))
    f = open(fn_qchem, 'r')
    atom = 0
    for line in f:
        if '$molecule' in line:
            for line in f:
                tokens = line.split()
                if len(tokens) < 2:
                    break
                elif len(tokens) == 4:
                    for j in range(3):
                        coords[atom][j] = float(tokens[j+1])
                    atom += 1
    f.close()
    return coords

def insert_qchem_rem_variable(qtemplate, variable, value):

    fn_in = qtemplate
    fn_out = qtemplate.strip()[:-3] + "_new.in"
    with open(fn_in, 'r') as input_file, open(fn_out, 'w') as output_file:
        for line in input_file:
            if '$rem' in line:
                output_file.write('$rem\n')
                output_file.write('%s        %s\n' % (variable, value))
            else:
                output_file.write(line)

def build_cube_input(qtemplate, coords, Nbasis, A_per_gp, box_space):

    xs = []
    ys = []
    zs = []
    for i in range(len(coords)):
        xs.append(coords[i][0])
        ys.append(coords[i][1])
        zs.append(coords[i][2])

    Ngp = []
    mins = []
    maxs = []
    mins.append(min(xs)-box_space)
    mins.append(min(ys)-box_space)
    mins.append(min(zs)-box_space)
    maxs.append(max(xs)+box_space)
    maxs.append(max(ys)+box_space)
    maxs.append(max(zs)+box_space)
    Ngp.append(round((maxs[0]-mins[0])/A_per_gp))
    Ngp.append(round((maxs[1]-mins[1])/A_per_gp))
    Ngp.append(round((maxs[2]-mins[2])/A_per_gp))

    MO_list = np.arange(Nbasis)
    fn_qchem = qtemplate
    with open(fn_qchem, 'a') as f:
        f.write('\n$plots\n')
        f.write('comment\n')
        for i in range(3):
            f.write('%d %4.2f %4.2f\n' % (Ngp[i], mins[i], maxs[i]))
        f.write('%d 0 0 0\n' % Nbasis)
        for i in MO_list:
            f.write('%d ' % (i+1))
        f.write('\n$end')

if __name__ == "__main__":

    variable = 'test_variable'
    value = 'TRUE'
    #coords = get_atom_positions(fn_qtemp, 2)
    #print coords
    #build_cube_input(fn_qtemp, coords, 36, 0.2, 4.0)
    insert_qchem_rem_variable(fn_qtemp, variable, value)
