#!/usr/bin/python

# Script to variationally minimize the energy w.r.t. temperature

import sys
import math
import matplotlib.pyplot as plt
from subprocess import check_call, check_output

if len(sys.argv) != 5:
        print "Usage: T_opt.py qchem-input temp-min temp-max num-temp-steps"
        exit(0)

filename = sys.argv[1]
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

def insert_temp(FON_file, temp, spin):

    if spin == 0:
        f_out = FON_file.strip()[:-4] + 'a.dat'
    else:
        f_out = FON_file.strip()[:-4] + 'b.dat'

    with open(FON_file, 'r') as input_file, open(f_out, 'w') as output_file:
        for line in input_file:
            tokens = line.split()
            tokens[2] = temp
            for i in range(len(tokens)):
                t = int(tokens[i])
                output_file.write('%d ' % (t))

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

    insert_temp('FON.dat', 1000, 0)
    insert_temp('FON.dat', 1000, 1)

#    for i in temps:
#        insert_temp('FONa.dat', i)
#        insert_temp('FONb.dat', i)
#        outputfile = run_qchem(filename)
