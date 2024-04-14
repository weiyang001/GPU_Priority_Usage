#!/bin/bash
var=0
ocp_memory=${1:-7000} # 程序需要的显存大小
# echo $ocp_memory
while [ $var -eq 0 ]
# echo 'waiting for available gpu...'
do
    count=0
    for i in $(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits)
    do
        # echo 'GPU'$i''
        size=$((12288-$i))
        # echo ''$size''
        if [ $ocp_memory -lt $size ]
        then
            echo 'GPU'$count' is avaiable'
            CUDA_VISIBLE_DEVICES=$count python train.py #将这一句更换为需要运行的程序
            var=1
            break
        fi
        count=$(($count+1))    
    done    
    if [ $var -eq 0 ]
    then
        sleep 10  # 在检查完所有GPU且没有找到符合条件的GPU后休眠10秒
done
