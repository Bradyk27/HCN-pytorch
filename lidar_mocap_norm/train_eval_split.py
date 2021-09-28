
import numpy as np
import os
import math
import random

pass_fail = 0
while not pass_fail:
    video_id = 999
    csv_files = [f for f in os.listdir('./') if f[len(f)-8::] == "skeleton"]
    random.shuffle(csv_files)
    eval_files = csv_files[0:math.floor(len(csv_files)/4)] #This determines split!
    subject_id_list = ['01','02','03','04','05','06','07','08','09'] #,'10']
    for file in eval_files:
        subject_id = file[file.find('subject')+7:file.find('subject')+9]
        try:
            subject_id_list.pop(subject_id_list.index(subject_id))
        except:
            pass
    if len(subject_id_list) == 0:
        for file in eval_files:
            subject_id = file[file.find('subject')+7:file.find('subject')+9]            
            os.rename(file, "video" + str(video_id) + "subject" + subject_id + ".skeleton")
            video_id += 1
        pass_fail = 1
