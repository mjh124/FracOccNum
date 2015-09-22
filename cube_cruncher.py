import numpy as np

def Extract_Preamble(filename):

    preamble = []
    fpre = open(filename, 'r')
    for line in fpre:
        tokens = line.split()
        if len(tokens) < 2:
            break
        preamble.append(line)
    return preamble

def Extract_Density(filename):

    MyData = open(str(filename), 'r')
    lines = MyData.readlines()[2:]
    MyData.close()

    dens = []
    for line in lines:
        tokens = line.split()
        if len(tokens) != 1:
            continue
        else:
            dens.append(float(tokens[0]))

    return dens

if __name__ == "__main__":
    
    prefix = 'Co13PCH3'
    total = prefix + '_total_aed.cube'
    ligand = prefix + '_ligand_aed.cube'
    core = prefix + '_core_aed.cube'

    preamble = Extract_Preamble(total)
    total_dens = Extract_Density(total)
    ligand_dens = Extract_Density(ligand)
    core_dens = Extract_Density(core)

    Ngrid = len(total_dens)
    binding_dens = [0.0 for i in range(Ngrid)]
    for i in range(Ngrid):
        binding_dens[i] = binding_dens[i] + total_dens[i] - (core_dens[i] + ligand_dens[i])

    fn_exc = prefix + '_binding_dens.cube'
    fout = open(fn_exc, 'w')
    for i in range(len(preamble)):
        fout.write(preamble[i])
    for i in range(Ngrid):
        fout.write('%20.10e\n' % binding_dens[i])
    fout.close()
