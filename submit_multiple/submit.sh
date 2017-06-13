#!/bin/bash

#SBATCH -J Cu_sub
#SBATCH -e job_err
#SBATCH -o job_out
#SBATCH -N 3
#SBATCH -p small
#SBATCH -t 01:00:00
#SBATCH --no-requeue
((ncores = 24 * SLURM_NNODES))

module load gpaw/0.10.0
module load gpaw-setups/0.8

aprun -n $ncores gpaw-python relax123.py
