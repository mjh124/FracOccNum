#!/bin/bash

temps="55000
60000
65000
70000"

for i in $temps
do
    mkdir $i"K"
    write_FON_files.py $i
    qchem -nt 4 "N2_1.11A.in" "N2_1.11A_"$i"K.out" "N2_1.11A"
    mv /tmp/qc-michael/N2_1.11A/plots/mo.*.cube ./$i"K"
    CISD_1RDM_fromQchem_faster.py 10 42 "N2_1.11A_"$i"K.out"

    mv "N2_1.11A_"$i"K_density.txt" ./$i"K"
    cd ./$i"K"
    #build_RealSpace_CISDDensity.py "N2_4.00A_"$i"K_density.txt" 52 2 56
    build_RealSpace_CISDDensity.py "N2_1.11A_"$i"K_density.txt" 52 2 56 5 5 28 2 14
    cd ../
done
