#!/bin/bash
arguments=($(python3 argfile.py))
file_string=""
num_files=${arguments[0]}
filepath=$(cd ../; pwd)

for ((i=0; i < $num_files; i++)); do
	file_string="${file_string[@]} -f ${arguments[$((i + 1))]}"
done

start_string="$(echo $file_string | sed -E "s/[ ]+//")"

keywords=("cache_size" "block_size" "associativity" "replacement_policy" "physical_memory")

offset=$((num_files + 1))

for word in ${keywords[@]}; do
	declare "$word=${arguments[$offset]}"
	((offset++))
done

args="${start_string:-"-f Trace1.trc"} -s ${cache_size:-512} -b ${block_size:-16} -a ${associativity:-8} -r ${replacement_policy:-"Random"} -p ${physical_memory:-4194304}"
python3 ../main.py $args
