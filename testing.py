import requests
import json

#^\[HorribleSubs\] (.*) \-\ ([0-9]+) \[(480|720|1080)#Regex

def main():
    response, codecs, container = create()
    print(response)
    print(codecs)
    print(container)
    if response == False:
        print('server is offline')
    else:
        wait_extension = input('Ekstensi File yang dikirim : ')
        wait_output_codecs = input('Output codecs yang dipilih : ')
        wait_output_container = input('Output container yang dipilih : ')
        wrap = wrapper(response,wait_extension,wait_output_codecs,wait_output_container)
        requests.get('http://'+ip_address+':'+port+'/start',params=wrap)
    
def create():
    colar = requests.get('http://'+ip_address+':'+port+'/create')
    try:
        colar.raise_for_status()
    except(requests.exceptions.HTTPError):
        return False
    resp = colar.json()
    response = str(resp['job'])
    avail_codecs = resp['codecs']
    container = resp['container']
    return response, avail_codecs, container

def wrapper(response,ext,codecs,container):
    collect = {'id': response, 'ext':ext, 'codecs':codecs,'container':container}
    return collect

if __name__ == '__main__':
    ip_address = input('Server IP Address : ')
    port = str(input('Server Port : '))
    try:
        while True:
            main()
            print('finish exec')
    except(KeyboardInterrupt):
        print('exiting program')