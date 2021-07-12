import numpy as np
import os
import math
import random

max_num = 58

skel_files = [f for f in os.listdir('./') if f[len(f)-8::] == "skeleton"]
skel_files.sort()
subject_labels = {}
for file in skel_files:
    subject_id = file[file.find('subject')+7:file.find('subject')+9]
    if subject_id not in subject_labels:
        subject_labels.update({subject_id:[file]})
    else:
        subject_labels[subject_id].append(file)

selected_files = []
for lab in subject_labels:
    random.shuffle(subject_labels[lab])
    for f in subject_labels[lab][:max_num]:
        selected_files.append(f)

for f in os.listdir('./'):
    if f[len(f)-8:] != "skeleton":
        continue
    if f not in selected_files:
        os.remove(f)
