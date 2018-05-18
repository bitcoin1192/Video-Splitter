import tornado.ioloop
import tornado.web
import random
import secrets
import search
import time
import threading
import ffmpeg as ff
import json
import shutil
import base64

class utama(tornado.web.RequestHandler):
    def get(self):
    #say hello to everyone    
        self.finish("Welcome To Backend API")

class acak(tornado.web.RequestHandler):
    def get(self):
        ngacak = secrets.token_urlsafe(16)
        proj_id.append([ngacak,0,time.time()])
        ff.create_folder(const,ngacak)
        ff.create_folder(const2,ngacak)
        ff.create_folder(const3,ngacak)
        content = json.dumps({'job' : ngacak}, separators=(',', ':'))
        #print(proj_id[len(proj_id)-1])
        self.finish(content)

class jobstart(tornado.web.RequestHandler):
    def get(self):
        var = self.get_argument('id', None)
        extension = self.get_argument('ext', None)
        if var or extension is None:
            self.set_status(404,reason='No id and extension given')
        arr = proj_id
        dem = search.edit_stats(arr, var)
        if dem is True:
        #Queueing pending job
            ready = [var,extension]
            search.queue_pass_array(ready)
            content = json.dumps({'job' : var}, separators=(',', ':'))
            print(var)
            self.finish(content)
        else:
            print('Accessing to Unknown ID')
            self.set_status(404,reason='Unknown ID')

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
                job, part = slave_queue.pop()
                content = json.dumps({'job' : job, 'part' : part}, separators=(',', ':'))
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
        if self.request.body:
            json_data = json.loads(self.request.body)
            proj_id = self.get_argument('proj_id')
            filename = str(list(json_data.keys())[0])
            binary_b64encoded = json_data[filename].encode('utf-8')
            try:
                binary = base64.b64decode(binary_b64encoded)
                with open(const3+proj_id+'/'+filename, "wb") as out:
                    out.write(binary)
                    out.close()
                self.set_status(200,reason='OK')
            except:
                self.set_status(404, reason='You didnt send anything')
        else:
            self.set_status(404, reason='You didnt send anything')

def main():
    application = tornado.web.Application([
        (r"/", utama),
        (r"/create", acak),
        (r"/start", jobstart),
        (r"/status", stats),
        (r"/slave", slave_comm),
        (r"/upload", upload_files)
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()

# Kode terpanjang dan terlama di program ini !
def ffmpeg_call():
    saat = True
    while saat is True:
        
        #[proj_id, status, time] array structure
        job = search.access_queue()
        if job is False:
            #print('No job, time for sleeping for 10 second')
            time.sleep(8)
        else:
            name, ext = job[0], job[1]
            #Return list of file
            result = search.search_file(const+str(name),ext)
            
            #result[0] will result in one string only
            ff.ffmpeg_call(const+name+'/'+result[0],const2+name)
            print('success running ffmpeg project ' + str(name))
            
            #Return list of file
            result_new = search.search_file(const2+str(name),"mp4")
            
            #check if result is not find
            if not result_new:
                print('can\'t find the split file on '+ const2+name)
            for i in result_new:
                slave_queue.append([name,i])
            result = search.search_file(const+str(name),ext)
            ff.ffmpeg_audio(const+name+'/'+result[0],const3+name)
    

if __name__ == "__main__":
    const = '/mnt/volume-sgp1-01/origin/'
    const2 = '/mnt/volume-sgp1-01/proj/'
    const3 = '/mnt/volume-sgp1-01/webm/'
    proj_id = []
    slave_queue = []
    thread = threading.Thread(target=ffmpeg_call, args=())
    thread.daemon = True # Daemonize thread
    thread.start()
    try:
        main()
    except(KeyboardInterrupt):
        shutil.rmtree(const)
        shutil.rmtree(const2)
        print('Program interupt. Deleting folder project')