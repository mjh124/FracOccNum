#!/usr/bin/python

# Script to generate all active space combinations with corresponding temperature
# Also drives qchem

import sys
import numpy as np
from subprocess import check_call
import collections

if len(sys.argv) != 2:
    print "Usage: extract_orbital_structure.py qchem_template"
    exit(0)

qtemplate = sys.argv[1]

###
# Run qchem
###

def run_qchem(filename):

    qchem = "runqchem.sh"
    input = filename
    output = filename.strip()[:-3] + ".out"
    args = input + " " + output
    print([qchem, args])
    check_call([qchem, args])
    return output

###
# Insert rem variable to skip SCFMAN
###

def insert_SKIP_SCFMAN(qtemplate):

    fn_in = qtemplate
    fn_out = qtemplate.strip()[:-3] + "_skip.in"
    with open(fn_in, 'r') as input_file, open(fn_out, 'w') as output_file:
        for line in input_file:
            if '$rem' in line:
                output_file.write('$rem\n')
                output_file.write('SKIP_SCFMAN        1\n')
            else:
                output_file.write(line)

###
# Extract total number of energy levels
###

def get_total_orbs(filename):

    fn_in = filename
    fin = open(fn_in, 'r')
    total_orbs_tmp = 0
    for line in fin:
        if "Occupied" in line:
            for line in fin:
                tokens = line.split()
                for i in range(len(tokens)):
                    if tokens[i] == '0.000':
                        total_orbs_tmp += 1
                if len(tokens) < 1:
                    break
    fin.close()
    total_orbs =  total_orbs_tmp / 2
    return total_orbs

###
# Extract total number of occupied energy levels
###

def get_numocc_orbs(filename):

    fn_in = filename
    fin = open(fn_in, 'r')
    num_occ_tmp = 0
    for line in fin:
        if "Occupied" in line:
            for line in fin:
                tokens = line.split()
                for i in range(len(tokens)):
                    if tokens[i] == '0.000':
                        num_occ_tmp += 1
                if "Virtual" in line:
                    break
    fin.close()
    num_occ = num_occ_tmp / 2
    return num_occ

if __name__ == '__main__':

    insert_SKIP_SCFMAN(qtemplate)
    input_scf_skip = qtemplate.strip()[:-3] + "_skip.in"
    output_scf_skip = run_qchem(input_scf_skip)

    num_occ = get_numocc_orbs(output_scf_skip)
    total_orbs = get_total_orbs(output_scf_skip)
    print num_occ, total_orbs
