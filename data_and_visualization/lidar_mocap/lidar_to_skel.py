#Scale up to multiple videos / subject. Should be easy enough, just find subjectID. For now just selecting 2 should work.
#Plenty of room for code cleaning & formatting, including opening files up and down. Nonetheless, this works.
import numpy as np
import os

csv_files = [f for f in os.listdir('./') if f[len(f)-3::] == "csv"]
csv_files.sort()
video_labels = []
for i in range(1, len(csv_files)+1):
    if len(str(i))==1:
        video_labels.append('video0'+str(i))
    else:
        video_labels.append('video'+str(i))

video_labels = video_labels[0::2]

for lab in video_labels:
    for file in csv_files:
        if file.find(lab) != -1:
            working_files = [file, csv_files[csv_files.index(file)+1]]
            subject_id = file[file.find('subject')+7:file.find('subject')+9]

            for each in working_files:
                with open(each, 'r') as f:
                    num_frames = len(f.readlines())
                with open(each, 'r') as f:
                    with open('video0'+str(working_files.index(each)+1) + 'subject' + subject_id + '.skeleton', 'a+') as n:
                        num_bodies = 1
                        trackingID = int(subject_id)
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
                        header = [clippedEdges, hlc, hls, hrc, hrs, isrest, lean1, lean2, ts]

                        n.write(str(num_bodies)+'\n')
                        n.write(str(trackingID)+'\n')
                        for item in header:
                            if header.index(item)==len(header)-1:
                                n.write(str(item))
                            else:
                                n.write(str(item)+' ')
                        n.write('\n'+str(num_joints)+'\n')


                        for i in range(num_frames):
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
                                n.write(str(trackingID)+'\n')
                                for item in header:
                                    if header.index(item)==len(header)-1:
                                        n.write(str(item))
                                    else:
                                        n.write(str(item) + ' ')
                                n.write('\n'+str(num_joints)+'\n')

