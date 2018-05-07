import os
import time
import subprocess

#Extract Video and subtitle and convert Audio to opus format
def ffmpeg_call(input,name):
    subprocess.call(['ffmpeg','-i',input,'-f','segment','-vcodec','copy','-an','-reset_timestamps','1','-map','0', name+'/OUTPUT%d_Orig.mp4'],shell=False)
    subprocess.call(['ffmpeg','-i',input,'-vn','-acodec', 'libopus', name+'/OUTPUT.opus'],shell=False)
    subprocess.call(['ffmpeg','-i',input,'-map','0:s:0', name +'/OUTPUT.ass'],shell=False)

#Create folder path for project
def create_folder(path,name):
    try:
        os.makedirs(str(path)+str(name))
    except(FileExistsError):
        return

def read_file_in_folder(folder_name):
    pass