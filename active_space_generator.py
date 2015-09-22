import ExtractOrbitalStructure
from subprocess import check_call, check_output

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
# Define all combinations of a given number (get num_occ and num_virt from qchem output; also add constaints)
###

def generate_orbital_pairs(num_occ, Nact_occ, Nact_virt):

    start_orb = num_occ - Nact_occ
    end_orb = num_occ + Nact_virt
    pairs = [(x, y) for x in range(start_orb, num_occ) for y in range(num_occ, end_orb)]
    return pairs

###
# Write the file in the proper format for qchem to read (#ActiveOrbs  #Electrons  Temp(K)  ListofOrbs-C++counting)
###

def write_file(num_spaces, orb_act, num_elec, temp, orb_list, spinpol=0):

    # num_spaces is an integer defining the number of active spaces
    # orb_act, num_elec, temp are arrays of len(num_spaces)
    # orb_list is a list of lists that include the orbitals in the active spaces

    if spinpol == 0:
        fn_out = "FONa.dat"
    elif spinpol == 1:
        fn_out = "FONb.dat"
    else:
        print "Invalid value for spin polarization"

    fout = open(fn_out, 'w')
    for i in range(num_spaces):
        a = orb_act[i]
        b = num_elec[i]
        c = temp[i]
        fout.write('%d %d %d' % (a, b, c))
        for j in range(len(orb_list[i])):
            d = orb_list[i][j] # find a way to print list of lists
            fout.write(' %d' % (d))
        fout.write('\n')
    fout.close()

###
# Use extract_orbital_structure.py to get orbital structure
###

def get_orb_struc(qtemplate, spin):

    ExtractOrbitalStructure.insert_SKIP_SCFMAN(qtemplate)
    input_scf_skip = qtemplate.strip()[:-3] + "_skip.in"
    output_scf_skip = run_qchem(input_scf_skip)
    num_alpha_occ = ExtractOrbitalStructure.get_num_alpha_orbs(output_scf_skip)
    num_beta_occ = 0
    if spin == 1:
        num_beta_occ = ExtractOrbitalStructure.get_num_beta_orbs(output_scf_skip)
    total_orbs = ExtractOrbitalStructure.get_total_orbs(output_scf_skip, spin)
    return num_alpha_occ, num_beta_occ, total_orbs

def extract_energy(filename):

    energy = check_output(['awk', '/Total energy in the final basis set/ {print $9}', filename])
    return energy
