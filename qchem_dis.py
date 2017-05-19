#!/usr/bin/python

# Script to variationally minimize the energy w.r.t. temperature

import sys
import math
import matplotlib.pyplot as plt
from subprocess import check_call, check_output

if len(sys.argv) != 6:
        print "Usage: T_opt.py qchem-input BL-min BL-max num-steps temp"
        exit(0)

filename = sys.argv[1]
BL_min = sys.argv[2]
BL_max = sys.argv[3]
num_steps = int(sys.argv[4])
temp = int(sys.argv[5])

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

def insert_BL(filename, temp):

    with open(filename, 'r') as input_file, open(filename, 'w') as output_file:
        for line in input_file:
            tokens = line.split()
            tokens[2] = temp
            for i in range(len(tokens)):
                output_file.write('%d ' % (tokens[i]))

def form_temps(t_min, t_max, num_steps):

    t_range = t_max - t_min
    step = float(t_range) / num_steps
    temps = []
    for i in range(num_steps+1):
        temp = math.floor(t_min + (i * step))
        temps.append(int(temp))
    return temps

if __name__ == "__main__":

    temps = form_temps(t_min, t_max, num_steps)
    print temps

    for i in temps:
        insert_temp('FONa.dat', i)
        insert_temp('FONb.dat', i)
        outputfile = run_qchem(filename, i)
