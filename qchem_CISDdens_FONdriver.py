#!/usr/bin/python

import sys
import numpy as np
import QchemInputManip
import CISD_1RDM_fromQchem_Mod
from subprocess import check_call, check_output

if len(sys.argv) != 4:
    print "Usage: qchem_CISDdens_FONdriver.py qtemplate Nocc Nvirt"
    exit(0)

fn_qchem = sys.argv[1]
Nocc = int(sys.argv[2])
Nvirt = int(sys.argv[3])

def run_qchem(filename, temp):

    qchem = "runqchem.sh"
    input = filename
    output = filename.strip()[:-3] + "_" + str(temp) + "K.out"
    tmp_dir = filename.strip()[:-3]
    args = input + " " + output + " " + tmp_dir
    print(qchem, args)
    check_call([qchem, args])
    return output

def write_FON(fn, temp):

    with open(fn, 'r') as f_in:
        line = f_in.readline()
        tokens = line.split()
    with open(fn, 'w') as f_out:
        tokens[2] = temp
        for i in range(len(tokens)):
            f_out.write('%d ' % (float(tokens[i])))

if __name__ == "__main__":

    coords = QchemInputManip.get_atom_positions(fn_qchem, 2)
    QchemInputManip.build_cube_input(fn_qchem, coords, 36, 0.2, 4.0)

    temps = np.arange(0, 50001, 5000)
    FON_files = ['FONa.dat', 'FONb.dat']
    for i in range(len(temps)):
        for j in FON_files:
            write_FON(j, temps[i])

        run_qchem(fn_qchem, temps[i])
        #print 'Calculating CISD Density Matrix for ', fn_out
        #DensMat = CISD_1RDM_fromQchem_Mod.build_CISD_DensMat(Nocc, Nvirt, fn_out)
