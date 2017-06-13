from ase import *
from ase.io import read
from ase.optimize import *
from gpaw import *
from ase.constraints import *

# Isomer signature

# File construction
xyz = 'G3_I' + str(iso) + '.xyz'
output = 'G3_I' + str(iso) + '.txt'
gpw = '../print_mult/G3/G3_I' + str(iso) + '.gpw'

# Grid spacing
h = 0.25

# System setup

atom = read(xyz)

atom.center(vacuum=6.0)
cell = atom.get_cell()

#Setting the grid spacing exactly at h
for i in range(3):
    cell[i,i] = round(cell[i,i]/4/h)*4*h
    atom.set_cell(cell)

calc = GPAW(h=h,
            xc ='PBE',
            kpts=(1,1,1),
            occupations=FermiDirac(0.05),
            spinpol=False,
            charge=-1.0,
            maxiter=250,
            nbands=-80,
            mixer=Mixer(0.1, 6),
            txt=output)

atom.set_calculator(calc)
atom.get_potential_energy()

# Converge unoccupied bands
calc.set(convergence={'bands':-75},
         fixdensity=True,
         eigensolver='cg')
calc.calculate()

calc.write(gpw, 'all')
