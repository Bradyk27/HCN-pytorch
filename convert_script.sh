#!/bin/bash                                                                                                                                                            
#SBATCH -N 3                                                                                                                                                                      
#SBATCH --job-name=convert_HCN                                                                                                                                                      
#SBATCH --output=convert_HCN.log                                                                                                                                                    
#SBATCH --mail-type=ALL                                                                                                                                                             
#SBATCH --mail-user=bradyakruse@gmail.com                                                                                                                                          

enable_lmod
module load container_env tensorflow-gpu/2.2.0

crun.tensorflow-gpu python3 ./feeder/bk_gendata.py --data_path lidar_mocap --out_folder lidar_mocap_convert

