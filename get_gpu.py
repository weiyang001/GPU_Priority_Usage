# author: muzhan
import os
import sys
import time
import argparse

# cmd = 'python train_stage_3.py --dataset_path="data/dataset/m1guelpf/nouns_images_40%" --num_epochs=20 --batch_size=32 --lr=1e-2 --num_class=240 --model_path="DivideMix/model/40%" --id="40%" --num_workers=4 --resnet="ResNet50" --image_column="image" --label_column="head"'
# cmd = 'test'

def parse_args():
    parser = argparse.ArgumentParser(description='等待GPU')
    parser.add_argument('--num_gpu', '--num_GPU', default=1, type=int, help='GPU数量')
    parser.add_argument('--interval', default=5, type=int, help='等待秒数')
    parser.add_argument('--t_pow', '--threshold_power', default=50, type=int, help='功率阈值')
    parser.add_argument('--t_mem', '--threshold_memory', default=3000, type=int, help='显存阈值')
    parser.add_argument('--cmd', '--command', default='echo "please add --cmd argument"')
    
    args = parser.parse_args()
    return args

# def gpu_info():
#     gpu_status = os.popen('nvidia-smi | grep %').read().split('|')
#     gpu_memory = int(gpu_status[2].split('/')[0].split('M')[0].strip())
# #     gpu_power = int(gpu_status[1].split('   ')[-1].split('/')[0].split('W')[0].strip())
#     try:
#         # 使用split和strip处理字符串，提取功率数字部分
#         gpu_power_str = gpu_status[1].split('   ')[-1].split('/')[0].split('W')[0].strip()
#         # 检查提取的字符串是否为数字
#         if gpu_power_str.isdigit():
#             gpu_power = int(gpu_power_str)
#         else:
#             gpu_power = None  # 如果不是数字，设为 None 或适当的默认值
#     except IndexError:
#         # 如果分割操作失败，同样设为 None 或错误处理
#         gpu_power = None
#     return gpu_power, gpu_memory


# 多GPU版本
def gpu_info(gpu_index=2):
    info = os.popen('nvidia-smi|grep %').read().split('\n')[gpu_index].split('|')
    try:
        # 使用split和strip处理字符串，提取功率数字部分
        power = info[1].split()[-3][:-1]
        # 检查提取的字符串是否为数字
        if power.isdigit():
            power = int(power)
        else:
            power = None  # 如果不是数字，设为 None 或适当的默认值
    except IndexError:
        # 如果分割操作失败，同样设为 None 或错误处理
        power = None
    memory = int(info[2].split('/')[0].strip()[:-3])
    return power, memory


def narrow_setup(args):
    flag = True
    i = 0
    while flag:  # set waiting condition
        for idx in range(args.num_gpu):
            gpu_power, gpu_memory = gpu_info(gpu_index=idx)
            if gpu_power is not None and (gpu_power < args.t_pow and gpu_memory < args.t_mem):
                flag = False
                break
            i = i % 5
            symbol = 'monitoring: ' + '>' * i + ' ' * (10 - i - 1) + '|'
            gpu_power_str = 'gpu power:%d W |' % gpu_power
            gpu_memory_str = 'gpu memory:%d MiB |' % gpu_memory
            sys.stdout.write('\r' + gpu_memory_str + ' ' + gpu_power_str + ' ' + symbol)
            sys.stdout.flush()
            time.sleep(args.interval)
            i += 1
    print('\n' + args.cmd)
    os.system(args.cmd)    

def main():
    args = parse_args()
    narrow_setup(args)

if __name__ == '__main__':
    main()