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

def download(i):
    print(i)
    out = str(i[1])
    ff.create_folder('proj/',i[0])
    ff.create_folder('encode/',i[0])
    part_download = requests.get('http://cdn.sisalma.com/'+i[0]+'/'+out, timeout=10000)
    if part_download is None:
        print('error in part_download')
        return False
    with open('proj/'+i[0]+'/'+out, mode='wb') as files:
        files.write(part_download.content)
    return True

def upload(i):
    out = str(os.path.splitext(i[1])[0])+'.webm'
    files = open('encode/'+i[0]+'/'+out, mode='rb').read()
    parameter = {'proj_id': i[0]}
    b64_files = base64.b64encode(files)
    b64_files_str = b64_files.decode('utf-8')
    try:
        datas = {out : b64_files_str}
        resp = requests.post('http://api.sisalma.com/upload', params = parameter, json = datas, timeout=10000)
        resp.raise_for_status()
        print('upload ok ...')
        return True
    except(requests.exceptions.HTTPError):
        print('upload fail...')
        return False

def get_job(cpu_c):
    list_job = []
    count = 0
    #loop as much as cpu core available
    while count < int(cpu_c):
        r = requests.get('http://api.sisalma.com/slave', timeout=10)
        try :
            r.raise_for_status()
        except(requests.exceptions.ConnectTimeout, requests.exceptions.HTTPError):    
            return list_job
        dict_responses = r.json()
        list_job.append(list(dict_responses.values()))
        count = count + 1
    if not list_job:
        return False
    else:
        return list_job

def ffmpeg_call(i):
    input, name = i[0], i[1]
    out = os.path.splitext(name)[0]
    subprocess.run(['ffmpeg','-i','proj/'+input+'/'+out+'.mp4','-crf','25','-b:v','1000k','-minrate','500k','-maxrate','1500k','encode/'+input+'/'+out+'.webm','-loglevel','quiet'])
    return True

def exit_gracefully(hostname,zone):
    try:
        subprocess.call(['gcloud','-q','compute','instances','delete',str(hostname),'--zone',str(zone)])
        exit('exit program...')
    except:
        print('Not gcloud')
        exit('exit program...')

def main():
    print('Running client.py')
    status = True
    while status == True:
        api = requests.get('http://api.sisalma.com/slave?test=1', timeout=1000)
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
            print('error in listjob')
            raise EnvironmentError
        
    #run function as much as jobs available at the same time
        with Pool(processes = len(list_job)-1) as p:
            try:
                p.map(download, list_job)
                p.map(ffmpeg_call, list_job)
                p.map(upload, list_job)
            except:
                print('error in pool')
                raise EnvironmentError
        
        shutil.rmtree('encode',ignore_errors=True)
        shutil.rmtree('proj',ignore_errors=True)

#source : https://stackoverflow.com/questions/31688646/get-the-name-or-id-of-the-current-google-compute-instance
def metadata_zone(hostname):
    metadata_server = 'http://metadata.google.internal/computeMetadata/v1/instance/'
    metadata_flavor = {'Metadata-Flavor' : 'Google'}
    #gce_id = requests.get(metadata_server + 'id', headers = metadata_flavor).text
    #gce_name = requests.get(metadata_server + 'hostname', headers = metadata_flavor).text
    #gce_machine_type = requests.get(metadata_server + 'machine-type', headers = metadata_flavor).text
    gce_location = requests.get(metadata_server + 'zone', headers = metadata_flavor).text
    return gce_location

if __name__ == '__main__':
    try:
        hostname = platform.node()
        zone = metadata_zone(hostname)
        cpu_count = multiprocessing.cpu_count()
        main()
    except(KeyboardInterrupt,EnvironmentError):
        shutil.rmtree('encode',ignore_errors=True)
        shutil.rmtree('proj',ignore_errors=True)
        print('Deleting Folder and instances NOW...')
        time.sleep(10)
        exit_gracefully(hostname,zone)
