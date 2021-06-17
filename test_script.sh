#!/bin/bash

#SBATCH -p gpu
#SBATCH --gres gpu:1
#SBATCH -N 1
#SBATCH --job-name=test_HCN
#SBATCH --output=test_HCN.log
#SBATCH --mail-type=ALL
#SBATCH --mail-user=bradyakruse@gmail.com

enable_lmod
module load container_env tensorflow-gpu/2.2.0

crun.tensorflow-gpu python -m visdom.server &
crun.tensorflow-gpu python3 main.py --dataset_dir skeleton_convert/ --mode test --load True --model_name HCN --dataset_name NTU-RGB-D-CV --num 01

## Need to figure out how to access visdom here!! When I can access it remotely, the HCN-PyTorch cannot. When I can't access it remotely, the HCN-PyTorch can. Something weird with GPU partition connections?
## Can only access visdom when NOT running on a gpu partition. Meanwhile, HCN-PyTorch can only access visdom when they are running on the SAME NODE within the gpu partition, or at least best I can tell.
