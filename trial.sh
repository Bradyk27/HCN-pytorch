#!/bin/bash
module load container_env tensorflow-gpu/2.2.0
rm *.out
for i in {1..20}
do
    rm lidar_mocap/*.skeleton
    crun.tensorflow-gpu python lidar_mocap/lidar_to_skel.py
    crun.tensorflow-gpu python lidar_mocap/train_eval_split.py
    crun.tensorflow-gpu python ./feeder/bk_gendata.py --data_path lidar_mocap --out_folder lidar_mocap_convert/lidar_mocap
    sbatch train_script.sh
    sleep 20m
done
    
    
