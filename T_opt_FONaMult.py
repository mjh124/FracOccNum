#!/usr/bin/python

# Script to variationally minimize the energy w.r.t. temperature

import sys
import math
import matplotlib.pyplot as plt
from subprocess import check_call, check_output

# Takes one T_max, one T_min, and one #steps, will make a square symmetric grid

if len(sys.argv) != 5:
        print "Usage: T_opt_FONa.py qchem-input temp-min temp-max num-temp-steps"
        print "Right now only written for two active spaces"
        exit(0)

inputfile = sys.argv[1]
t_min = int(sys.argv[2])
t_max = int(sys.argv[3])
num_steps = int(sys.argv[4])

###
# Run qchem
###

def run_qchem(filename, temp1, temp2):

    qchem = "runqchem.sh"
    input = filename
    output = filename.strip()[:-3] + "_" + str(temp1) + "K_" + str(temp2) + "K.out"
    args = input + " " + output
    print(qchem, args)
    check_call([qchem, args])
    return output

###
# Extract total energy
###

def extract_energy(filename):

    energy = check_output(['awk', '/Total energy in the final basis set/ {print $9}', filename])
    return energy

###
# Check for convergence
###

def convergence_check(filename):

    outfile = open(filename, 'r')
    outlines = outfile.readlines()
    outfile.close()
    message = "Have a nice day."

    conv = False
    for line in outlines:
        if message in line:
            conv = True
        else:
            continue

    return conv

###
# Define array of temperatures
###

def form_temps(t_min, t_max, num_steps):
    
    t_range = t_max - t_min
    step = float(t_range) / num_steps
    temps = []
    for i in range(num_steps+1):
        temp = math.floor(t_min + (i * step))
	temps.append(int(temp))
    return temps

###
# Parse FONa.dat
###

def parse_FONa():

    fn_FON = 'FONa.dat'
    Norbs = []
    Nel = []
    temp = []
    occ_orb = []
    virt_orb = []
    with open(fn_FON, 'r') as f:
        lines = f.readlines()
        for line in lines:
            tokens = line.split()
            Norbs.append(int(tokens[0]))
            Nel.append(int(tokens[1]))
            temp.append(int(tokens[2]))
            occ_orb.append(int(tokens[3]))
            virt_orb.append(int(tokens[4]))
    return Norbs, Nel, temp, occ_orb, virt_orb

###
# Write FONa.dat
###

def write_FONa(Norbs, Nel, temp, occ_orb, virt_orb):

    fn_FON = 'FONa.dat'
    with open(fn_FON, 'w') as fout:
        for i in range(len(Norbs)):
            fout.write('%d %d %d %d %d\n' % (Norbs[i], Nel[i], temp[i], occ_orb[i], virt_orb[i]))

###
# Main code
###

if __name__ == '__main__':
   
    temps = form_temps(t_min, t_max, num_steps)
    print temps
    Norbs, Nel, temp, occ_orb, virt_orb = parse_FONa()

    for i in temps:
        temp[0] = i
        for j in temps:
            temp[1] = j
            write_FONa(Norbs, Nel, temp, occ_orb, virt_orb)

            outputfile = run_qchem(inputfile, i, j)
            convergence = convergence_check(outputfile)
            print convergence
