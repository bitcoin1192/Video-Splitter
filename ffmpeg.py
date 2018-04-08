import os
import time
import subprocess

def ffmpeg_call(input,name):
    subprocess.call(['ffmpeg','-i',name,'*','-f segment -vcodec copy -an -reset_timestamps 1 -map 0 /mnt/volume-sgp1-01/proj/',name,'/OUTPUT%d_Orig.mp4'])
    subprocess.call(['ffmpeg','-i',name,'*','-vn -acodec libopus /mnt/volume-sgp1-01/proj/',name,'/OUTPUT.opus'])

def create_folder(name):
    os.makedirs("/mnt/volume-sgp1-01/"+str(name))

def read_file_in_folder(folder_name):
    pass