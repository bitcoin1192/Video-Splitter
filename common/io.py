import requests
from ffmpeg import ffmpeg as ff
import base64
import os
import json
import re

def download(i):
    print(i)
    out = str(i[1])
    ff.create_folder(['proj/'],i[0])
    ff.create_folder(['encode/'],i[0])
    part_download = requests.get('http://cdn.sisalma.com/'+i[0]+'/'+out, timeout=8000)
    if part_download is None:
        print('error in part_download')
        return False
    with open('proj/'+i[0]+'/'+out, mode='wb') as files:
        files.write(part_download.content)
    return True

def upload(i):
    out = str(os.path.splitext(i[1])[0])+'.'+str(i[3])
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

def upload_emergency(i):
    data = i    
    try:
        datas = {'out' : data}
        resp = requests.post('http://api.sisalma.com/cancel', json = datas, timeout=10000)
        resp.raise_for_status()
        print('upload ok ...')
        return True
    except(requests.exceptions.HTTPError):
        print('upload fail...')
        return False

'''def upload_stream(i):
    out = str(os.path.splitext(i[1])[0])+'.webm'
    parameter = {'proj_id': i[0]}
    with open('encode/'+i[0]+'/'+out, mode='rb') as files:
        b64_files = base64.b64encode(files.read())
        b64_files_str = b64_files.decode('utf-8')
    try:
        datas = {out : b64_files_str}
        resp = requests.post('http://api.sisalma.com/upload', params = parameter, json = datas, timeout=10000)
        resp.raise_for_status()
        print('upload ok ...')
        return True
    except(requests.exceptions.HTTPError):
        print('upload fail...')
        return False'''