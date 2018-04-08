#import requests
import http.client
#import http
import re
import time
import json
import codecs

conn = http.client.HTTPConnection("localhost",port=8888)
#conn1 = requests.get("http://localhost:8888/create")
def start():
    print('ready for testing')
    print('press enter to start')
    return main()

def main():
    p = re.compile("/'(.*?)'/s")
    counter = 0
    step = 0
    state = False
    array = []
    while state is False:
        if step == 0:#create job
            conn.request("GET", "/create", headers={'Content-type':'application/json'})
            jobid = conn.getresponse()
            ww = p.match(str(jobid.read()))
            ss = json.loads(codecs.open(ww,mode="r",encoding="utf-8"))
            array.append(ss)
            print(array)
            if jobid.status == 500:
                print("error while creating job")
                time.sleep(10000)
            if counter == 100:
                step = 1
                counter = 0
                print("succesfully create jobid")
            counter += 1
        elif step == 1:#verify status
            for a in array:
                conn.request("GET", "/status?jobid="+str(a))
                content = conn.getresponse()
                if content == "wot":
                    print("jobid not being inserted correctly")
                    time.sleep(10000)
            state = True
            #time.sleep(10000)
    print("Test Success")
    time.sleep(10000)

start()
        #elif step == 2:#start
        #    start = conn.request("GET", "/start?jobid="+)
        #    if counter == 1200:
        #        state = True
