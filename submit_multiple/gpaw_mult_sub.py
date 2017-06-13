#!/usr/bin/env python

import sys
import numpy as np

if len(sys.argv) != 4:
    print "Usage: gpaw_mult_submit.py  gpaw-template  submisson-script-template  number-isomers"
    exit(0)

gtemp = sys.argv[1]
sub_temp = sys.argv[2]
N = int(sys.argv[3])

def insert_ISOMER(gtemp, sig):

    fn_in = gtemp
    fn_out = gtemp.strip()[:-3] + "_I" + str(sig) + ".py"
    with open(fn_in, 'r') as input_file:
        with open(fn_out, 'w') as output_file:
            for line in input_file:
                if 'Isomer signature' in line:
                    output_file.write('# Isomer signature\n')
                    output_file.write('iso = ' + str(sig) + '\n')
                else:
                    output_file.write(line)

def write_submit(sub_temp, sig):

    fn_in = sub_temp
    fn_out = sub_temp.strip()[:-3] + "_I" + str(sig) + ".sh"
    with open(fn_in, 'r') as input_file:
        with open(fn_out, 'w') as output_file:
            for line in input_file:
                if 'aprun' in line:
                    output_file.write('aprun -n $ncores gpaw-python unocc_I' + str(sig) + '.py')
                else:
                    output_file.write(line)


if __name__ == "__main__":

    signatures = np.arange(N)

    for i in signatures:
        iso = i + 1
        insert_ISOMER(gtemp, iso)
        write_submit(sub_temp, iso)
