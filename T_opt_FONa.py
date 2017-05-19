#!/usr/bin/python

# Script to variationally minimize the energy w.r.t. temperature

import sys
import math
import matplotlib.pyplot as plt
from subprocess import check_call, check_output

if len(sys.argv) != 5:
        print "Usage: T_opt_FONa.py qchem-input temp-min temp-max num-temp-steps"
        exit(0)

inputfile = sys.argv[1]
t_min = int(sys.argv[2])
t_max = int(sys.argv[3])
num_steps = int(sys.argv[4])

###
# Run qchem
###

def run_qchem(filename, temp):

    qchem = "runqchem.sh"
    input = filename
    output = filename.strip()[:-3] + "_" + str(temp) + "K.out"
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
# Replace temperature in FONa.dat file
###

def get_lines():

    fn_in = 'FONa.dat'
    with open(fn_in, 'r') as input_file:
        lin = input_file.readline()
        tokens = lin.split()
    print tokens
    return tokens

def replace_line(tokens, temp):

    fn_out = 'FONa.dat'
    with open(fn_out, 'w') as output_file:
        tokens[2] = temp
        for i in range(len(tokens)):
            val = float(tokens[i])
            output_file.write('%d ' % (val))

###
# Main code
###

if __name__ == '__main__':
   
    temps = form_temps(t_min, t_max, num_steps)
    print temps
    en = []
    temperatures = []
    for i in temps:

        contents = get_lines()
        replace_line(contents, i)

        outputfile = run_qchem(inputfile, i)

        convergence = convergence_check(outputfile)
        print convergence
