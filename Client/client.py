import http.client
import re
import time
import json
import codecs
import subprocess
import os
import requests

global id
global part

def download(file,path):
    link = "/"+path+'/'+file
    lls = cdn.request("GET", link, headers={'Content-type':'application/json'})
    if lls is None:
        return False
    return True

def upload(file,path):
    link = "/"+path+'/'+file
    with open('/'+file, 'rb') as byte:
        lls = cdn.request("PUT", link, body=byte, headers={'Content-type':'octet-stream/webm'})
    return True

def something():
    link = api.request("GET", "/slave", headers={'Content-type':'application/json'})
    jobid = link.getresponse()
    result = json.load(jobid)
    if result is None:# after 1 fail attempt shutdown instances immediately
        return None, None
    id = result['id']
    part = result['part']
    return id, part
    
def ffmpeg_call(input):
    subprocess.call(['ffmpeg','-i',input,'-f','segment','-vcodec','copy','OUTPUT%d_Orig.webm'])

def main():
    global api
    global cdn
    try:
        api = requests.get('http://api.sisalma.com', timeout=10)
        cdn = requests.get('http://cdn.sisalma.com')
        api.raise_for_status()
    except (requests.exceptions.ConnectTimeout, requests.exceptions.HTTPError):
        print('error handled')
        os.system('echo 1 > /proc/sys/kernel/sysrq && echo b > /proc/sysrq-trigger')
    id, part = something()
    if id is None:
        os.system('echo 1 > /proc/sys/kernel/sysrq && echo b > /proc/sysrq-trigger')
    ffmpeg_call(id+'mp4')
    upload(id,part)

main()