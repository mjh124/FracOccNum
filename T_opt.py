#!/usr/bin/python

# Script to variationally minimize the energy w.r.t. temperature

import sys
import math
import matplotlib.pyplot as plt
from subprocess import check_call, check_output

if len(sys.argv) != 5:
        print "Usage: T_opt.py qchem-input temp-min temp-max num-temp-steps"
        exit(0)

qtemplate = sys.argv[1]
t_min = int(sys.argv[2])
t_max = int(sys.argv[3])
num_steps = int(sys.argv[4])

###
# Run qchem
###

def run_qchem(filename):

    qchem = "runqchem.sh"
    input = filename
    output = filename.strip()[:-3] + ".out"
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
# Replace temperature in qchem input
###

def replace_temp(filename, temp):

    fn_in = filename + '.in'
    fn_out = filename + '_' + str(temp) + '.in'
    with open(fn_in, 'r') as input_file, open(fn_out, 'w') as output_file:
        for line in input_file:
            if 'fon_t_start' in line:
                line.strip()
                output_file.write('fon_t_start    %d\n' % (temp))
            elif 'fon_t_end' in line:
                line.strip()
                output_file.write('fon_t_end    %d\n' % (temp))
            else:
                output_file.write(line)

###
# Main code
###

if __name__ == '__main__':
   
    filename = qtemplate.strip()[:-3]

    temps = form_temps(t_min, t_max, num_steps)
    print temps
    en = []
    temperatures = []
    for i in temps:

        replace_temp(filename, i)
        inputfile = filename + '_' + str(i) + '.in'
        outputfile = run_qchem(inputfile)

        convergence = convergence_check(outputfile)
        print convergence

        if convergence == True:
            energy = extract_energy(outputfile)
            en.append(float(energy))
            temperatures.append(i)
        else:
            continue

    print "temperatures =", temperatures
    print "energies =", en
    plt.scatter(temperatures, en, s=50, c='k')
    plt.xlabel('Temperature (K)')
    plt.ylabel('Energy (Ha)')
    plt.show()
