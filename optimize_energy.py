#!/usr/bin/python

# Qchem FON-calculation driver and optimizer

import sys
import numpy as np
from scipy.optimize import minimize # or whatever I need
import ExtractOrbitalStructure
import active_space_generator

if len(sys.argv) != 4:
    print "Usage: optimize_energy.py qchem_input_template Nact_occ Nact_virt"
    exit(0)

qtemplate = sys.argv[1]
Nact_occ = int(sys.argv[2])
Nact_virt = int(sys.argv[3])

###
# Get energy
###

def get_energy(temp, spin, qtemplate):

    num_spaces = Nact_occ * Nact_virt
    orb_act = [2 for i in range(num_spaces)]
    num_elec = [1 for i in range(num_spaces)]
    temp = [temp for i in range(num_spaces)]

    alpha_pairs = active_space_generator.generate_orbital_pairs(alpha_occ, Nact_occ, Nact_virt)
    active_space_generator.write_file(num_spaces, orb_act, num_elec, temp, alpha_pairs)
    if spin == 1:
        beta_pairs = active_space_generator.generate_orbital_pairs(beta_occ, Nact_occ, Nact_virt)
        active_space_generator.write_file(num_spaces, orb_act, num_elec, temp, beta_pairs, spinpol=spin)

    input_file = qtemplate # Fix this to account from whatever the filename is
    output_file = active_space_generator.run_qchem(input_file)

    energy = active_space_generator.extract_energy(output_file)

    return energy

###
# Minimize energy w.r.t. temperature
###
#
#def minimize_energy(E, T_start, T_end):
#
#    What function to use?
#    xtol - convergence tolerance
#    scipy.optimize(fun=..., x0='initial guess', method='Nelder-Mead', xtol='conv tol')

###
# Main function
###

if __name__ == "__main__":

    spin = ExtractOrbitalStructure.check_spin(qtemplate)
    alpha_occ, beta_occ, total_orbs = active_space_generator.get_orb_struc(qtemplate, spin)
    print alpha_occ, beta_occ, total_orbs

    if Nact_occ > alpha_occ:
        exit("ERROR: Too many occupied orbitals requested in active space")
    elif total_orbs < (alpha_occ + Nact_virt):
        exit("ERROR: Too many virtual orbitals requested in active space")

    energy = get_energy(1000.0, spin, qtemplate) # Works like this, include temperature more systematically
    print "Energy =",energy
