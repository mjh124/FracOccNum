#!/bin/bash

temps="0
5000
10000
15000
20000
25000
30000
35000
40000
45000
50000"

for i in $temps
do
    mkdir $i"K"
    write_FON_files.py $i
    qchem -nt 4 "N2_1.50A.in" "N2_1.50A_"$i"K.out" "N2_1.50A"
    mv /tmp/qc-michael/N2_1.50A/plots/mo.*.cube ./$i"K"
    CISD_1RDM_fromQchem.py 10 22 "N2_1.50A_"$i"K.out"

    mv "N2_1.50A_"$i"K_density.txt" ./$i"K"
    cd ./$i"K"
    build_RealSpace_CISDDensity.py "N2_1.50A_"$i"K_density.txt" 32 2 36

    cd ../
done
