import time
import subprocess
import os
import requests
import platform
import multiprocessing
from multiprocessing import Pool
import ffmpeg as ff
import shutil


def download(job):
    for i in job:
        ff.create_folder('proj/',i[0])
        ff.create_folder('encode/',i[0])
        part_download = requests.get('http://cdn.sisalma.com/'+i[0]+'/'+i[1], timeout=10)
        if part_download is None:
            return False
        with open('proj/'+i[0]+'/'+i[1], mode='wb') as files:
            files.write(part_download.content)
    return True

def upload(i):
    #input, name = i[0], i[1]
    out = os.path.splitext(i[1])[0]
    multifiles = [('video', (out+'.webm', open('encode/'+i[0]+'/'+out+'.webm', mode='rb')), 'video/webm')]
    requests.post('http://api.sisalma.com/upload?proj_id='+i[0],files = multifiles, timeout=10)
    return True

def get_job(cpu_c):
    list_job = []
    count = 0
    
    #loop as much as needed
    while count <= int(cpu_c):
        r = requests.get('http://api.sisalma.com/slave', timeout=10)
        try :
            r.raise_for_status()
        except (requests.exceptions.ConnectTimeout, requests.exceptions.HTTPError):    
            return list_job
        dict_responses = r.json()
        list_job.append(list(dict_responses.values()))
        count = count + 1
    return list_job

def something():
    result = get_job(cpu_count)
    
    # after 1 fail attempt shutdown instances immediately
    if result is None:
        return None
    return result

def ffmpeg_call(i):
    input, name = i[0], i[1]
    out = os.path.splitext(name)[0]
    subprocess.call(['ffmpeg','-i','proj/'+input+'/'+out+'.mp4','encode/'+input+'/'+out+'.webm'])

def main():
    global cpu_count
    status = True
    while status == True:
        #Check cpu core count and hostname
        hostname = platform.node()
        cpu_count = multiprocessing.cpu_count()
        
        #check if main server is not ready
        try:
            api = requests.get('http://api.sisalma.com/slave?test=1', timeout=10)
            api.raise_for_status()
        
        #delete instances as soon as eception encountered 
        except (requests.exceptions.ConnectTimeout, requests.exceptions.HTTPError):
            print('error handled, deleting this instance')
            subprocess.call(['gcloud','-q','compute','instances','delete',hostname,'--zone','asia-southeast1-a'])
            exit('woops')
        
        #check for job availability
        list_job = something()
        if list_job is None:
            subprocess.call(['gcloud','-q','compute','instances','delete',hostname,'--zone','asia-southeast1-a'])
            exit('woops')
        
        #download media file
        res = download(list_job)
        if res is False:
            subprocess.call(['gcloud','-q','compute','instances','delete',hostname,'--zone','asia-southeast1-a'])
        
        #run function as much as jobs available at the same time
        with Pool(processes = len(list_job)-1) as p:
            p.map(ffmpeg_call, list_job)
            p.map(upload, list_job)
        
        shutil.rmtree('encode',ignore_errors=True)
        shutil.rmtree('proj',ignore_errors=True)

if __name__ == '__main__':
    main()