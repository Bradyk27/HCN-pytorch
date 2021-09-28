import numpy as np
import argparse
import os
import sys
from ntu_read_skeleton import read_xyz
from numpy.lib.format import open_memmap
import pickle
import re

#01, 02, 03? Do we need to specify training subjects as well?
#training_subjects = [1,2,3,4,5,6,7,8,9,10]
training_videos = list(range(1,999)) #This determines train / val split. Hardcoded currently
max_body = 1
num_joint = 13
max_frame = 3
toolbar_width = 30


def print_toolbar(rate, annotation=''):
    #Why not just use tqdm????
    sys.stdout.write("{}[".format(annotation))
    for i in range(toolbar_width):
        if i * 1.0 / toolbar_width > rate:
            sys.stdout.write(' ')
        else:
            sys.stdout.write('-')
        sys.stdout.flush()
    sys.stdout.write(']\r')


def end_toolbar():
    sys.stdout.write("\n")


def gendata(data_path,
            out_path,
            ignored_sample_path=None,
            benchmark='xvid',
            part='eval'):
    
    if ignored_sample_path != None:
        with open(ignored_sample_path, 'r') as f:
            ignored_samples = [
                line.strip() + '.skel' for line in f.readlines()
            ]
    else:
        ignored_samples = []
    sample_name = []
    sample_label = []
    for filename in os.listdir(data_path):
        if filename[len(filename)-8:] != "skeleton":
            continue
        if filename in ignored_samples:
            continue
        subject_id = int(
            filename[filename.find('subject') + 7:filename.find('subject') + 9])
        video_id = int(
            re.findall(r'\d+', filename[filename.find('video') + 5:filename.find('video') + 9])[0]) #Not scalable...but should work.

        if benchmark == 'xvid':
            istraining = (video_id in training_videos)
            
        #elif benchmark == 'xsub':
        #   istraining = (subject_id in training_subjects)
        else:
            raise ValueError()

        if part == 'train':
            issample = istraining
        elif part == 'val':
            issample = not (istraining)
        else:
            raise ValueError()

        if issample:
            sample_name.append(filename)
            sample_label.append(subject_id - 1) #-1? I assume some indexing later on

    with open('{}/{}_label.pkl'.format(out_path, part), 'wb') as f:
        pickle.dump((sample_name, list(sample_label)), f)
    
    fp = open_memmap(
        '{}/{}_data.npy'.format(out_path, part),
        dtype='float32',
        mode='w+',
        shape=(len(sample_label), 3, max_frame, num_joint, max_body))

    fl = open_memmap(
        '{}/{}_num_frame.npy'.format(out_path, part),
        dtype='int',
        mode='w+',
        shape=(len(sample_label),))

    for i, s in enumerate(sample_name):
        print_toolbar(i * 1.0 / len(sample_label),
                      '({:>5}/{:<5}) Processing {:>5}-{:<5} data: '.format(
                          i + 1, len(sample_name), benchmark, part))
        data = read_xyz(
            os.path.join(data_path, s), max_body=max_body, num_joint=num_joint)
        fp[i, :, 0:data.shape[1], :, :] = data

        fl[i] = data.shape[1]
    end_toolbar()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='LIDAR MOCAP Data Converter.')
    parser.add_argument('--data_path', default='/lidar_mocap')
    parser.add_argument('--ignored_sample_path', default=None)
    parser.add_argument('--out_folder', default='/lidar_mocap_convert/lidar_mocap')

    benchmark = ['xvid']
    part = ['train', 'val']
    arg = parser.parse_args()

    for b in benchmark:
        for p in part:
            out_path = os.path.join(arg.out_folder, b)
            if not os.path.exists(out_path):
                os.makedirs(out_path)
            gendata(
                arg.data_path,
                out_path,
                arg.ignored_sample_path,
                benchmark=b,
                part=p)
