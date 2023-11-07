#!/bin/bash

file_list=(file1.trc file2.trc file3.trc)
file_string=""
for file in ${file_list[@]}; do file_string="$file_string -f $file"; done

cache_size=512
block_size=16
associativity=8
replacement_policy=Random
physical_memory=4194304

python3 main.py $file_string -s $cache_size -b $block_size -a $associativity -r $replacement_policy -p $physical_memory
