function write_skeleton_for_CNN

files = dir();

for file_index = 3:length(files)
    
    extension = files(file_index).name(end-2:end);
    
    if strcmp(extension,'csv')
        
        csv_file_name = files(file_index).name;
        
        video_str = csv_file_name(6:7);
        subject_str = csv_file_name(15:16);
        subject_number = str2double(subject_str);
        
        
        
        temp = readmatrix(csv_file_name);
        
        number_of_frames = size(temp,1);
        skeleton_data = zeros(number_of_frames,13,3);
        
        for frame = 1:number_of_frames
            skeleton_data(frame,:,:) = reshape(temp(frame,:),3,13)';
        end
        
        file_name = ['video',video_str,'subject',subject_str,'.skel'];
        write_skeleton(skeleton_data,file_name,subject_number);
        
    end
    
end

end

function write_skeleton(skeleton_data,file_name,subject_number)

fileid = fopen(file_name,'wt');
framecount = size(skeleton_data,1);
fprintf(fileid,'%d ',framecount); % no of the recorded frames

for f=1:framecount
    bodycount = 1;
    fprintf(fileid,'%d ',bodycount); % no of observerd skeletons in current frame
    for b=1:bodycount
        clear body;
        body.bodyID = subject_number;
        fprintf(fileid,'%ld ',body.bodyID); % tracking id of the skeleton
        
        
        %if it's unknown, I just use 0
        body.clipedEdges = 0;
        body.handLeftConfidence = 0;
        body.handLeftState = 0;
        body.handRightConfidence = 0;
        body.handRightState = 0;
        body.isResticted = 0;
        arrayint = [body.clipedEdges,body.handLeftConfidence,body.handLeftState,body.handRightConfidence,body.handRightState,body.isResticted];
        fprintf(fileid,'%ld ',arrayint); % 6 integers
        
        
        
        body.leanX = 0;
        body.leanY = 0;
        lean = [body.leanX,body.leanY];
        fprintf(fileid,'%f ',lean);
        
        body.trackingState = 0;
        fprintf(fileid,'%d ',body.trackingState);
        
        body.jointCount = 13;
        fscanf(fileid,'%d ',body.jointCount); % no of joints original(25)
        
        for j=1:body.jointCount
            
            
            
            % 3D location of the joint j
            joint.x = skeleton_data(f,j,1);
            joint.y = skeleton_data(f,j,2);
            joint.z = skeleton_data(f,j,3);
            jointinfo(1) = joint.x;
            jointinfo(1) = joint.y;
            jointinfo(1) = joint.x;
            
            
            % 2D location of the joint j in corresponding depth/IR frame
            joint.depthX = 0;
            jointinfo(4) = joint.depthX;
            joint.depthY = 0;
            jointinfo(5) = joint.depthY;
            
            % 2D location of the joint j in corresponding RGB frame
            joint.colorX = skeleton_data(f,j,1);
            jointinfo(6)=joint.colorX;
            joint.colorY = skeleton_data(f,j,2);
            jointinfo(7)=joint.colorY;
            
            % The orientation of the joint j
            joint.orientationW = 0;
            jointinfo(8) = joint.orientationW;
            joint.orientationX = 0;
            jointinfo(9) = joint.orientationX;
            joint.orientationY = 0;
            jointinfo(10) = joint.orientationY;
            joint.orientationZ = 0;
            jointinfo(11) = joint.orientationZ;
            
            fprintf(fileid,'%lf ',jointinfo);
            
            % The tracking state of the joint j
            joint.trackingState = 0;
            
            fprintf(fileid,'%d ',joint.trackingState);
            
            
        end
        
    end
end
fclose(fileid);
end