#!/bin/bash
#set -x
set -u
cdir="all_results"
mkdir $cdir
for dir in $(ls $1)
do 
if [ -f $dir  ] ;then #escape if dir is a file
continue
fi
prefix=${dir%%[^0-9]*}	  
file=$dir"/results.csv"
cp $1$dir"/results.csv"  $cdir"/"$prefix"_results.csv"
echo "copied "$prefix"_results.csv"

done
echo "finished copying"

