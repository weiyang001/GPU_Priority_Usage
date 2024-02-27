#!/bin/bash
var=0
ocp_memory=${1:-500}
while [ $var -eq 0 ]
echo 'waiting for available gpu...'
do
    count=0
    for i in $(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits)
    do
        echo 'GPU'$i''
        if [ $i -lt $ocp_memory ]
        then
            echo 'GPU'$count' is avaiable'
            CUDA_VISIBLE_DEVICES=$count python /U_PZL2022KF0005/home/wangweiyu/Second/train/train01/train.py --cuda --gpu 6 --epoches 4 --batchSize 16 --lr 1e-4 --style_content_loss --recon_loss --tv_loss --recon_ws_ssim_loss --ws_ssim_loss --temporal_loss --data_sigma --data_w
            var=1
            break
        fi
        count=$(($count+1))    
    done    
done
