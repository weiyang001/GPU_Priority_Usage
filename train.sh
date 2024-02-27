#!/bin/bash
var=0
ocp_memory=${1:-500}
while [ $var -eq 0 ]
# echo 'waiting for available gpu...'
do
    count=0
    for i in $(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits)
    do
        # echo 'GPU'$i''
        size=$((81920-$i))
        # echo ''$size''
        if [ $i -lt $size ]
        then
            echo 'GPU'$count' is avaiable'
            CUDA_VISIBLE_DEVICES=$count python train.py #
            var=1
            break
        fi
        count=$(($count+1))    
    done    
done
