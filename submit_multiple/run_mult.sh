#!/bin/bash

gpaw_mult_sub.py unocc.py submit.sh $1

for i in $(seq $1)
do
    JOB=submit_I$i.sh
    sbatch $JOB
    echo "submitted $JOB"
done
