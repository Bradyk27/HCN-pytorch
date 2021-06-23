

"""
@author: huguyuehuhu, edited by bradyk27
@time: 18-4-12 下午3:10
Permission is given to modify the code, any problem please contact huguyuehuhu@gmail.com
"""
import torch
from feeder.feeder import Feeder
import numpy as np

def fetch_dataloader(types, params):
    """
    Fetch and return train/dev
    """
    if 'lidar_mocap' in params.dataset_name :
            params.train_feeder_args["data_path"] = params.dataset_dir+'lidar_mocap'+'/xvid/train_data.npy'
            params.train_feeder_args["num_frame_path"] = params.dataset_dir+'lidar_mocap'+'/xvid/train_num_frame.npy'
            params.train_feeder_args["label_path"] = params.dataset_dir + 'lidar_mocap' + '/xvid/train_label.pkl'
            params.test_feeder_args["data_path"] = params.dataset_dir + 'lidar_mocap' + '/xvid/val_data.npy'
            params.test_feeder_args["num_frame_path"] = params.dataset_dir + 'lidar_mocap' + '/xvid/val_num_frame.npy'
            params.test_feeder_args["label_path"] = params.dataset_dir + 'lidar_mocap' + '/xvid/val_label.pkl'

    if types == 'train':
        if not hasattr(params,'batch_size_train'):
            params.batch_size_train = params.batch_size

        loader = torch.utils.data.DataLoader(
            dataset=Feeder(**params.train_feeder_args),
            batch_size=params.batch_size_train,
            shuffle=True,
            num_workers=params.num_workers,pin_memory=params.cuda)

    if types == 'test':
        if not hasattr(params,'batch_size_test'):
            params.batch_size_test = params.batch_size

        loader = torch.utils.data.DataLoader(
            dataset=Feeder(**params.test_feeder_args),
            batch_size=params.batch_size_test ,
            shuffle=False,
            num_workers=params.num_workers,pin_memory=params.cuda)

    return loader

if __name__ == '__main__':

    pass
