#Scale up to multiple videos / subject. Should be easy enough, just find subjectID. For now just selecting 2 should work.
#Plenty of room for code cleaning & formatting, including opening files up and down. Nonetheless, this works.
import numpy as np
import os
import math

csv_files = [f for f in os.listdir('./') if f[len(f)-3::] == "csv"]
csv_files.sort()
subject_labels = {}
for file in csv_files:
    subject_id = file[file.find('subject')+7:file.find('subject')+9]
    if subject_id not in subject_labels:
        subject_labels.update({subject_id:[file]})
    else:
        subject_labels[subject_id].append(file)

for lab in subject_labels:
    video_lab = 1
    for file in subject_labels[lab]:
        with open(file, 'r') as f:
            total_num_frames = len(f.readlines())

        with open(file, 'r') as f:
            for i in range(math.floor(total_num_frames / 10)):
                with open('video'+str(video_lab) + 'subject' + lab + '.skeleton', 'a+') as n:
                    num_bodies = 1
                    num_frames = 10
                    trackingID = int(lab)
                    clippedEdges = 0
                    hlc = 0
                    hls = 0
                    hrc = 0
                    hrs = 0
                    isrest = 0
                    lean1 = 0
                    lean2 = 0
                    ts = 2
                    num_joints = 13
                    
                    n.write(str(num_frames)+'\n')
                    header = [trackingID, clippedEdges, hlc, hls, hrc, hrs, isrest, lean1, lean2, ts]

                    n.write(str(num_bodies)+'\n')
                    for item in header:
                        if header.index(item)==len(header)-1:
                            n.write(str(item))
                        else:
                            n.write(str(item)+' ')
                    n.write('\n'+str(num_joints)+'\n')


                    for i in range(10):
                        line = f.readline().strip('\n').split(',')
                        for j in range(0, (num_joints*3),3):
                            x = line[j]
                            y = line[j+1]
                            z = line[j+2]
                            depthX = 0
                            depthY = 0
                            colorX = x
                            colorY = y
                            oW = 0
                            oX = 0
                            oY = 0
                            oZ = 0
                            ts = 2

                            skel_line = [x,y,z,depthX,depthY,colorX,colorY,oW,oX,oY,oZ,ts]

                            for item in skel_line:
                                if item == '-0':
                                    item = '0'
                                if skel_line.index(item)==len(skel_line)-1:
                                    n.write(str(item))
                                else:
                                    n.write(str(item) + ' ')
                            n.write('\n')

                        if i != num_frames-1:
                            n.write(str(num_bodies)+'\n')
                            
                            for item in header:
                                if header.index(item)==len(header)-1:
                                    n.write(str(item))
                                else:
                                    n.write(str(item) + ' ')
                            n.write('\n'+str(num_joints)+'\n')
                video_lab+=1
        #dawgs by a million
