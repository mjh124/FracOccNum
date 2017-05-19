#!/usr/bin/python

# Script that takes a list of discrete data points, broadens each with a Gaussian, and returns the sum

import sys
import numpy as np

if len(sys.argv) != 5:
    print "Usage: GaussianBroadener.py input-file fermi-level(Ha) broadening-amount(eV) output-file"
    exit(0)

fn_in = sys.argv[1]
ef = float(sys.argv[2])
sig = float(sys.argv[3])
fn_out = sys.argv[4]

###
# Parse dos file from cp2k. Ignores first 2 lines so make sure no data until 3rd line
###
def parse_input_file(fn_in):

    Ha2eV = 27.2114
    with open(fn_in, 'r') as f:
        lines = f.readlines()[2:]
        en = []
        s_dos = []
        p_dos = []
        d_dos = []
        for line in lines:
            tokens = line.split()
            en.append(Ha2eV*(float(tokens[1])-ef))
            s_dos.append(float(tokens[3]))
            p_dos.append(float(tokens[4]))
            d_dos.append(float(tokens[5]))
    return en, s_dos, p_dos, d_dos

###
# Broaden each state with a gaussian and weight with given state
###
def GaussianBroaden(sig, en, dos):

    x_mat = len(en)
    y_mat = len(x_axis)

    gauss_broad = np.zeros(y_mat)
    for i in range(y_mat):
        tmp = 0.0
        for j in range(x_mat):
            gauss = dos[j]*np.exp(-((x_axis[i]-en[j])/sig)**2)
            tmp += gauss
        gauss_broad[i] = gauss_broad[i] + tmp
    return gauss_broad

###
# Call previous functions and plot
###
if __name__ == '__main__':

    en, s_dos, p_dos, d_dos = parse_input_file(fn_in)
#    print en, s_dos
    
    plt.clf()
    x_axis = np.arange(-40, 175, 0.2) #Step size must be </=sigma or the broadening will not work properly
    plt.axis([-40, 100, 0.0, 3.0]) #Adjust here to control plotting interval. If broadening value is changed y-max will change.

    gauss_s = GaussianBroaden(sig, en, s_dos)
    gauss_p = GaussianBroaden(sig, en, p_dos)
    gauss_d = GaussianBroaden(sig, en, d_dos)

    with open(fn_out, 'w') as f:
        for i in range(len(en)):
            f.write("%12.10f  %12.10f  %12.10f  %12.10f\n" % (energy, gauss_s[i], gauss_p[i], gauss_d[i]))
