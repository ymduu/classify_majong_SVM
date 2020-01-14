#!/bin/sh
c=0
for image in $(ls . | grep .png$ ); do
    #echo "${image}"
    python preprocess.py "${image}" $c
    c=`expr $c + 1`
done
