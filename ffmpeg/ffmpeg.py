import os
import time
import subprocess
import ffprobe3

#Extract Video and subtitle and convert Audio to opus format
#'-loglevel','quiet'
def ffmpeg_call(input,name):
    subprocess.run(['ffmpeg','-i',input,'-f','segment','-c','copy','-an','-sn','-reset_timestamps','0',name+'/OUTPUT%d_Orig.mp4'],shell=False)

def ffmpeg_audio(input,name):
    subprocess.run(['ffmpeg','-i',input,'-vn','-sn','-ac','2','-b:a','128k','-vbr','on', name+'/OUTPUT.opus'],shell=False)
    subprocess.run(['ffmpeg','-i',input,'-vn','-an', name +'/OUTPUT.ass'],shell=False)

#Create folder path for project
def create_folder(path,name):
    try:
        for i in path:
            os.makedirs(str(path)+str(name))
        return True
    except(FileExistsError):
        return 'Already eksist'

def ff_stitch(name):
    subprocess.run(['ffmpeg','-f','concat','-safe','0','-i',name+'index','-c','copy',name+'output.webm'],shell=False)
    subprocess.run(['ffmpeg','-y','-i',name+'output.webm','-i',name+'OUTPUT.opus','-c:v','copy','-c:a','copy','/mnt/volume-sgp1-01/cdn/test.webm'],shell=False)

def check_valid(container, codecs):
    if container == 'mp4':
        valid_codecs = ['x264','x265']
        for i in valid_codecs:
            if codecs == i:
                return True
        return False
    if container == 'webm':
        valid_codecs = ['libvp9','libvp8']
        for i in valid_codecs:
            if codecs == i:
                return True
        return False
    return False