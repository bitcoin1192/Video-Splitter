import os
import time
import subprocess

#Extract Video and subtitle and convert Audio to opus format
#'-loglevel','quiet'
def ffmpeg_call(input,name):
    subprocess.run(['ffmpeg','-i',input,'-f','segment','-vcodec','copy','-an','-sn','-reset_timestamps','1',name+'/OUTPUT%d_Orig.mp4','-loglevel','quiet'],shell=False)

def ffmpeg_audio(input,name):
    subprocess.run(['ffmpeg','-i',input,'-vn','-sn','-acodec', 'libopus', name+'/OUTPUT.opus','-loglevel','quiet'],shell=False)
    subprocess.run(['ffmpeg','-i',input,'-vn','-an', name +'/OUTPUT.ass','-loglevel','quiet'],shell=False)

#Create folder path for project
def create_folder(path,name):
    try:
        os.makedirs(str(path)+str(name))
    except(FileExistsError):
        return

def ff_stitch(name):
    subprocess.run(['ffmpeg','-f','concat','-safe','0','-i',name+'index','-c','copy',name+'output.webm'],shell=False)
    subprocess.run(['ffmpeg','-y','-i',name+'output.webm','-i',name+'OUTPUT.opus','-c:v','copy','-c:a','copy','/mnt/volume-sgp1-01/cdn/test.webm'],shell=False)


#ffmpeg -f concat -safe 0 -i mylist.txt -c copy output