import tornado.ioloop
import tornado.web
import random
import secrets
from common import search, fileiterator
import time
import threading
from ffmpeg import ffmpeg as ff
import json
import shutil
import base64

class utama(tornado.web.RequestHandler):
    def get(self):   
        self.finish("Welcome To Backend API")

class acak(tornado.web.RequestHandler):
    def get(self):
        ngacak = secrets.token_urlsafe(16)
        proj_id.append([ngacak,0,time.time()])
        list = [const,const2,const3]
        ff.create_folder(list,ngacak)
        codecs = ['libvp9','libvp8','x264','x265']
        container = ['mp4','webm']
        content = json.dumps({'job' : ngacak,'codecs':str(codecs),'container':str(container)}, separators=(',', ':'))
        self.finish(content)

class jobstart(tornado.web.RequestHandler):
    def get(self):
        try:
            var, extension = self.get_argument('id'),self.get_argument('ext').lower
            codecs, container = self.get_argument('codecs').lower,self.get_argument('container').lower
            arr = proj_id
            dem = search.edit_stats(arr, var)
            validity = ff.check_valid(container,codecs)
            if validity is False:
                self.set_status(404, reason='Non valid combination between codec and container')
            if dem is True:
            #Insert job to queue
                ready = [var,extension,codecs,container,0]#[str,str,str,str,typefile]
                search.queue_pass_array(ready)
                content = json.dumps({'job' : var}, separators=(',', ':'))
                print(ready)
                self.finish(content)
            else:
                print('Accessing to Unknown ID')
                self.set_status(404,reason='Unknown ID')
        except(tornado.web.MissingArgumentError):
            self.set_status(404,reason='No extension or id were given')

class stats(tornado.web.RequestHandler):
    def get(self):
        var = self.get_argument('id', None)
        a, b = search.find(proj_id, var)
        if a is None:
            print('Accessing to Unknown ID')
            self.set_status(404,reason='Unknown ID')
        else:
            var = str(a[1])
            count = str(b)
            print(var + count)
            self.finish(var)
        

class slave_comm(tornado.web.RequestHandler):
    def get(self):
        var = self.get_argument('test',None)
        if not var:
            try:
                job, part, codecs, container, resolution = slave_queue.pop()
                content = json.dumps({'job' : job, 'part' : part, 'encoder': codecs, 'container': container, 'resolution':resolution}, separators=(',', ':'))
                self.finish(content)
            except(IndexError):
                self.set_status(404,reason='no job')
        else:
            try:
                cool = len(slave_queue)
                if cool == 0 :
                    raise IndexError
                else:
                    print('There is job available')
                    self.set_status(200, reason='ok')
            except(IndexError):
                print('Zero Job to do')
                self.set_status(404, reason='no video to be encode')

class upload_files(tornado.web.RequestHandler):
    #source https://techoverflow.net/2015/06/09/upload-multiple-files-to-the-tornado-webserver/
    def post(self):
        setting = self.get_argument('set',0)
        if int(setting) == 1:
            path = const
        else:
            path = const3
        if self.request.body:
            proj_id = self.get_argument('proj_id')
            json_data = json.loads(self.request.body)
            filename = str(list(json_data.keys())[0])
            binary_b64encoded = json_data[filename].encode('utf-8')
            try:
                binary = base64.b64decode(binary_b64encoded)
                with open(path+proj_id+'/'+filename, "wb") as out:
                    out.write(binary)
                    out.close()
                self.set_status(200,reason='OK')
            except:
                self.set_status(500, reason='There was problem writing to '+proj_id)
        else:
            self.set_status(404, reason='You didnt send anything')

class cancel_process(tornado.web.RequestHandler):
    def post(self):
        if self.request.body:
            json_data = json.loads(self.request.body)
            hasil = list(json_data['out'])
            print(hasil)
            if not hasil:
                self.set_status(500, reason='Fail parsing json data')
            else:
                for i in hasil:
                    slave_queue.append(i)
                #    filename = json_data[i]
                #    slave_queue.append([i,filename])
                self.set_status(200, reason='Insert to slave_queue succesful')
        else:
            self.set_status(404, reason='Unknown payload')


def main():
    application = tornado.web.Application([
        (r"/", utama),
        (r"/create", acak),
        (r"/start", jobstart),
        (r"/status", stats),
        (r"/slave", slave_comm),
        (r"/upload", upload_files),
        (r"/cancel", cancel_process)
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()

# Kode terpanjang dan terlama di program ini !
def ffmpeg_call():
    saat = True
    print('ff_call started')
    while saat is True:
        
        #[proj_id, status, time] array structure
        job = search.access_queue()
        if job is False:
            time.sleep(8)
        else:
            name, ext, codecs, container, tipe = job[0], job[1], job[2], job[3], job[4]
            if tipe == 0:
                #Return list of file
                result = search.search_file(const+str(name),ext)
                
                #result[0] will result in one string only
                ff.ffmpeg_call(const+name+'/'+result[0],const2+name)
                print('success running ffmpeg project ' + str(name))
                
                #Find framesize
                w_res, resolution = ff.check_resolution(const+name+'/'+result[0])
                res = ['2160','1440','1080','720','360','240','144']
                
                #total file * count(resolution)   
                count = 0
                for i in res:
                    if i <= resolution:
                        count += count
                    else:
                        pass
                        
                #Return list of file
                result_new = search.search_file(const2+str(name),"mkv")
                queue_status.append([name,(len(result_new))*count])
                #check if result is not find
                if not result_new:
                    print('can\'t find the split file on '+ const2+name)
                for i in result_new:
                    slave_queue.append([name,i,codecs,container,resolution])

                result = search.search_file(const+str(name),ext)
                ff.ffmpeg_audio(const+name+'/'+result[0],const3+name)
                shutil.rmtree(const+name+'/')
            else:
                ff.ff_stitch(const3+name+'/')

    
def other_routine():
    ss = True
    print('stitch routine started')
    while ss is True:
        if not queue_status:
            pass
        else:
            lists = queue_status.pop()
            name, file = lists[0],lists[1]
            result_new = search.search_file(const3+str(name),"webm")
            if len(result_new) >= int(file):
                print('start stitching video')
                fileiterator.listfilebyformats(const3+name,'webm')        
                search.queue_pass_array([name,'webm',1])
            else:
                queue_status.append(lists)
        time.sleep(10)

if __name__ == "__main__":
    const = '/mnt/volume-sgp1-01/origin/'
    const2 = '/mnt/volume-sgp1-01/proj/'
    const3 = '/mnt/volume-sgp1-01/webm/'
    proj_id = []
    slave_queue = []
    queue_status = []
    thread = threading.Thread(target=ffmpeg_call, args=())
    thread2 = threading.Thread(target=other_routine, args=())
    thread2.daemon = True
    thread.daemon = True # Daemonize thread
    thread.start()
    thread2.start()
    try:
        main()
    except(KeyboardInterrupt):
        shutil.rmtree(const)
        shutil.rmtree(const2)
        print('Program interupt. Deleting folder project')