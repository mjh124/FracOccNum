#!/bin/bash

dist="1.0
1.1
1.25
1.4
5.0"

for i in $dist
do
    head -n3 n2_temp.inp > begin.txt
    insert="N 0.0 0.0 "$i
    echo $insert >> begin.txt
    tail -n11 n2_temp.inp > end.txt
    cat begin.txt end.txt > "N2_"$i"A.inp"
done
