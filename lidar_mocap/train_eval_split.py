import numpy as np
import os
import math
import random

video_id = 999
csv_files = [f for f in os.listdir('./') if f[len(f)-8::] == "skeleton"]
random.shuffle(csv_files)
eval_files = csv_files[0:math.floor(len(csv_files)/4)] #This determines split!
for file in eval_files:
    subject_id = file[file.find('subject')+7:file.find('subject')+9]
    os.rename(file, "video" + str(video_id) + "subject" + subject_id + ".skeleton")
    video_id += 1
print(video_id)
