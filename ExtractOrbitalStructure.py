###
# Insert rem variable to skip SCFMAN
###

def insert_SKIP_SCFMAN(qtemplate):

    fn_in = qtemplate
    fn_out = qtemplate.strip()[:-3] + "_skip.in"
    with open(fn_in, 'r') as input_file, open(fn_out, 'w') as output_file:
        for line in input_file:
            if '$rem' in line:
                output_file.write('$rem\n')
                output_file.write('SKIP_SCFMAN        1\n')
            else:
                output_file.write(line)

###
# Check for spin restriction
###

def check_spin(qtemplate):

    fn_in = qtemplate
    fn_out = qtemplate.strip()[:-3] + "_skip.in"
    spin = 0
    with open(fn_in, 'r') as input_file:
        for line in input_file:
            test = line.lower()
            tokens = test.split()
            if len(tokens) != 2:
                continue
            elif tokens[0] == "unrestricted" and tokens[1] == "true":
                spin = 1
            else:
                continue

    return spin

###
# Extract total number of energy levels
###

def get_total_orbs(filename, spin):

    fn_in = filename
    fin = open(fn_in, 'r')
    total_orbs_tmp = 0
    for line in fin:
        if "Occupied" in line:
            for line in fin:
                tokens = line.split()
                for i in range(len(tokens)):
                    if tokens[i] == '0.000':
                        total_orbs_tmp += 1
                if len(tokens) < 1:
                    break
    fin.close()
    if spin == 1:
        total_orbs =  total_orbs_tmp / 2
    else:
        total_orbs = total_orbs_tmp

    return total_orbs

###
# Get number of occupied alpha orbitals
###

def get_num_alpha_orbs(filename):

    fin = open(filename, 'r')
    num_alpha_occ = 0

    for line in fin:
        if "Alpha MOs" in line:
            for line in fin:
                if "Occupied" in line:
                    continue
                tokens = line.split()
                if "Virtual" in line:
                    break
                num_alpha_occ += len(tokens)
    fin.close()

    return num_alpha_occ

###
# Get number of occupied beta orbitals
###

def get_num_beta_orbs(filename):

    fin = open(filename, 'r')
    num_beta_occ = 0

    for line in fin:
        if "Beta MOs" in line:
            for line in fin:
                if "Occupied" in line:
                    continue
                tokens = line.split()
                if "Virtual" in line:
                    break
                num_beta_occ += len(tokens)
    fin.close()
            
    return num_beta_occ
