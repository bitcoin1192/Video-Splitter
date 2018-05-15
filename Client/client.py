import time
import subprocess
import os
import requests
import platform
import multiprocessing
from multiprocessing import Pool
import ffmpeg as ff
import shutil
import base64
import time


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
    b16_files = base64.b16encode(files)
    print(b16_files)
    try:
        datas = {out : b16_files}
        resp = requests.post('http://api.sisalma.com/upload',params = parameter, json = datas, timeout=10000)
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
    subprocess.run(['ffmpeg','-i','proj/'+input+'/'+out+'.mp4','encode/'+input+'/'+out+'.webm','-loglevel','quiet'])
    return True

def exit_gracefully():
    #hostname = platform.node()
    try:
        #subprocess.call(['gcloud','-q','compute','instances','delete',hostname,'--zone','asia-southeast1-a'])
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
if __name__ == '__main__':
    try:
        cpu_count = multiprocessing.cpu_count()
        main()
    except(KeyboardInterrupt):
        shutil.rmtree('encode',ignore_errors=True)
        shutil.rmtree('proj',ignore_errors=True)
        print('Deleting Folder and instances NOW...')
        time.sleep(10)
        exit_gracefully()
