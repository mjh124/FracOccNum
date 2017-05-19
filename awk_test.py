#!/usr/bin/python

import sys
from subprocess import check_call, check_output

if len(sys.argv) != 2:
    print "Usage: awk_test.py filename"
    exit(0)

fn = sys.argv[1]

def extract_CISDenergy(fn):

    message = "Total energy ="
    states = []
    with open(fn, 'r') as f:
        for line in f:
            if message in line:
                states.append(float(line.split()[3]))
    return states[0]

def extract_energy(filename):

    # Extracts CISD ground state energy only
    CISD_enArray = check_output(['awk', '/Total energy = / {print $4}', filename])
    energy = float(CISD_enArray[:13])
    return energy

if __name__ == "__main__":

    energy = extract_CISDenergy(fn)
    print energy
