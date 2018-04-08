import os
import time
import subprocess

def ffmpeg_call(name):
    subprocess.call(['ffmpeg','-i',name,'*','-f segment -vcodec copy -an -reset_timestamps 1 -map 0 u/',name,'/OUTPUT%d_Orig.mp4'])
    subprocess.call(['ffmpeg','-i',name,'*','-vn -acodec aac u/',name,'/OUTPUT.aac'])

def create_folder(name):
    os.makedirs("u/"+str(name))

def read_file_in_folder(folder_name):
    pass