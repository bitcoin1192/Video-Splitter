import requests
import json

#^\[HorribleSubs\] (.*) \-\ ([0-9]+) \[(480|720|1080)#Regex

def main():
    response = create()
    print(response)
    if response == False:
        print('server is offline')
    else:
        wait_extension = input('Ekstensi File yang dikirim : ')
        wrap = wrapper(response,wait_extension)
        requests.get('http://api.sisalma.com/start',params=wrap)
    
def create():
    colar = requests.get('http://api.sisalma.com/create')
    try:
        colar.raise_for_status()
    except(requests.exceptions.HTTPError):
        return False
    resp = colar.json()
    response = str(resp['job'])
    return response

def wrapper(response,ext):
    collect = {'id': response, 'ext':ext}
    return collect

if __name__ == '__main__':
    try:
        while True:
            main()
            print('finish exec')
    except(KeyboardInterrupt):
        print('exiting program')