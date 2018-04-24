import http.client
import re
import time
import json
import codecs
import subprocess
import os

global id
global part

def download(file,path):
    link = "/"+path+'/'+file
    lls = conn.request("GET", link, headers={'Content-type':'application/json'})
    if lls is None:
        return False
    return True

def upload(file,path):
    link = "/"+path+'/'+file
    with open('/'+file, 'rb') as byte:
        lls = conn.request("PUT", link, body=byte, headers={'Content-type':'octet-stream/webm'})
    return True

def something():
    link = conn.request("GET", "/slave", headers={'Content-type':'application/json'})
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
    global conn
    global conn1
    try:
        conn = http.client.HTTPConnection('api.sisalma.com',port=80)
        conn1 = http.client.HTTPConnection('cdn.sisalma.com',port=80)
    except ConnectionRefusedError or TimeoutError:
        print('error handled')
        os.system('echo 1 > /proc/sys/kernel/sysrq && echo b > /proc/sysrq-trigger')
    id, part = something()
    if id is None:
        os.system('echo 1 > /proc/sys/kernel/sysrq && echo b > /proc/sysrq-trigger')
    ffmpeg_call(id+'mp4')
    upload(id,part)

main()