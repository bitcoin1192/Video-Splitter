import time
import subprocess
import os
import requests
import platform
import multiprocessing
from multiprocessing import Pool
from ffmpeg import ffmpeg as ff
import shutil
import base64
import time
import json
from common import io



def main():
    global list_job
    print('Running client.py')
    status = True
    while status == True:
        api = requests.get('http://api.sisalma.com/slave?test=1', timeout=13000)
    #check if main server is not ready
        try:
            api.raise_for_status()
        
    #delete instances as soon as exception encountered 
        except (requests.exceptions.ConnectTimeout, requests.exceptions.HTTPError):
            print('Server is not running')
            raise EnvironmentError
        
    #check for job availability
        list_job = get_job(cpu_count)
        if list_job is None:
            print('error in fetching job')
            raise EnvironmentError
        
    #run pool mp for paralelization
        with Pool(processes = len(list_job)-1) as p:
            try:
                p.map(io.download, list_job)
                p.map(ffmpeg_call, list_job)
                p.map(io.upload, list_job)
            except:
                print('error in pool')
                raise EnvironmentError
        
        shutil.rmtree('encode',ignore_errors=True)
        shutil.rmtree('proj',ignore_errors=True)

def get_job(cpu_c):
    list_job = []
    count = 0
    #loop as much as cpu core available
    while count < int(cpu_c):
        r = requests.get('http://api.sisalma.com/slave', timeout=10000)
        try :
            r.raise_for_status()
        except(requests.exceptions.ConnectTimeout, requests.exceptions.HTTPError):    
            return list_job
        dict_responses = r.json()
        list_job.append(list(dict_responses.values()))
        count = count + 1
    if not list_job:
        return None
    else:
        return list_job

def ffmpeg_call(i):
    input, name = i[0], i[1]
    out = os.path.splitext(name)[0]
    subprocess.run(['ffmpeg','-i','proj/'+input+'/'+out+'.mp4','-crf','25','-b:v','1000k','-minrate','500k','-maxrate','1500k','encode/'+input+'/'+out+'.webm','-loglevel','quiet'])
    return True

def exit_gracefully(hostname,zone):
    emergency()
    try:
        #subprocess.call(['gcloud','-q','compute','instances','delete',str(hostname),'--zone',str(zone)])
        exit('exit program...')
    except:
        print('Not gcloud')
        exit('exit program...')

#source : https://stackoverflow.com/questions/31688646/get-the-name-or-id-of-the-current-google-compute-instance
def metadata_zone(hostname):
    metadata_flavor = {'Metadata-Flavor' : 'Google'}
    gce_location = requests.get(metadata_server + 'zone', headers = metadata_flavor).text
    return gce_location

def check_preemptible():
    metadata_flavor = {'Metadata-Flavor' : 'Google'}
    while True:
        gce_status = requests.get(metadata_server + 'preempted', headers = metadata_flavor).text
        if gce_status == 'TRUE':
            raise EnvironmentError
        else:
            pass
        time.sleep(2)

def emergency():
    io.upload_emergency(list_job)


if __name__ == '__main__':
    hostname = platform.node()
    zone = metadata_zone(hostname)
    cpu_count = multiprocessing.cpu_count()
    metadata_server = 'http://metadata.google.internal/computeMetadata/v1/instance/'
    try:
        main()
    except(KeyboardInterrupt,EnvironmentError):
        shutil.rmtree('encode',ignore_errors=True)
        shutil.rmtree('proj',ignore_errors=True)
        print('Deleting Folder and instances NOW...')
        time.sleep(3)
        exit_gracefully(hostname,zone)
