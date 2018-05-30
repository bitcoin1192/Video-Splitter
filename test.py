import time 
import requests

def check_preemptible():
    metadata_server = 'http://metadata.google.internal/computeMetadata/v1/instance/'
    metadata_flavor = {'Metadata-Flavor' : 'Google'}
    print('Checking for preemptible')
    while True:
        gce_status = requests.get(metadata_server + 'preempted', headers = metadata_flavor).text
        if gce_status == 'TRUE':
            print('Being preempted')
            raise EnvironmentError
        else:
            pass
        time.sleep(2)

check_preemptible()