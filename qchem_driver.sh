#!/bin/bash

for i in $(seq 0 5000 100000)
do
    for j in $(seq 0 5000 100000)
    do
        write_FON_files.py $i $j
        qchem -nt 4 "N2_3.50A.in" "N2_3.50A_"$i"K_"$j"K.out"
     done
done
#    mkdir $i"K"
#    write_FON_files.py $i $j
#    qchem -nt 4 "N2_1.11A.in" "N2_1.11A_"$i"K.out" "N2_2.50A"
#    mv /tmp/qc-michael/N2_2.50A/plots/mo.*.cube ./$i"K"
#    CISD_1RDM_fromQchem_faster.py 10 42 "N2_2.50A_"$i"K.out"
#
#    mv "N2_2.50A_"$i"K_density.txt" ./$i"K"
#    cd ./$i"K"
#    #build_RealSpace_CISDDensity.py "N2_4.00A_"$i"K_density.txt" 52 2 56
#    build_RealSpace_CISDDensity.py "N2_2.50A_"$i"K_density.txt" 52 2 56 5 5 28 2 14
#    cd ../
#done
