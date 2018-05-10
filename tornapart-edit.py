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

class utama(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world")

class acak(tornado.web.RequestHandler):
    def get(self):
        ngacak = secrets.token_urlsafe(16)
        proj_id.append([ngacak,0,time.time()])
        ff.create_folder(const,ngacak)
        ff.create_folder(const2,ngacak)
        print(proj_id[len(proj_id)-1])
        self.write(str(ngacak))
        self.finish()

class jobstart(tornado.web.RequestHandler):
    def get(self):
        var = self.get_argument('id')
        arr = proj_id
        dem = search.edit_stats(arr, var)
        if dem is True:
            #Queueing pending job
            search.queue_pass_array(var)
            print(var)
            self.write(str(var))
            self.finish()
        else:
            print('Accessing to Unknown ID')
            self.write_error(404)
            self.finish()

class stats(tornado.web.RequestHandler):
    def get(self):
        var = self.get_argument('id')
        a, b = search.find(proj_id, var)
        if a is None:
            print('Accessing to Unknown ID')
            self.write_error(404)
            self.finish
        else:
            var = str(a[1])
            count = str(b)
            print(var + count)
            self.write(var)
            self.finish
        

class slave_comm(tornado.web.RequestHandler):
    def get(self):
        var = self.get_argument('test',None)
        if not var:
            try:
                job, part = slave_queue.pop()
                content = json.dumps({'job' : job, 'part' : part}, separators=(',', ':'))
                self.write(content)
                self.finish()
            except(IndexError):
                self.set_status(404)
        else:
            try:
                cool = len(slave_queue)
                if cool == 0 :
                    raise IndexError
                else:
                    self.set_status(200)
                    self.finish('ok')
            except(IndexError):
                self.set_status(404)
                self.finish('nope')

class upload_files(tornado.web.RequestHandler):
    #source https://techoverflow.net/2015/06/09/upload-multiple-files-to-the-tornado-webserver/
    def post(self):
        print('someone uploading file to this server')
        files = []
        try:
            files = self.request.files['files']
            proj_id = self.get_argument('proj_id')
        except:
            self.set_status(404, reason='You didnt upload anything')
        for xfile in files:
            filename = xfile['filename']
            with open(const2+proj_id+'/'+filename, "wb") as out:
                out.write(xfile['file'])
        self.set_status(200,reason='OK')

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
            print('No job, time for sleeping for 10 second')
            time.sleep(15)
        else:
            #Return list of file
            result = search.search_file(const+str(job),"mp4")
            
            #result[0] will result in one string only
            ff.ffmpeg_call(const+job+'/'+result[0],const2+job)
            print('success running ffmpeg project ' + str(job))
            
            #Return list of file
            result_new = search.search_file(const2+str(job),"mp4")
            
            #check if result is not find
            if not result_new:
                print('can\'t find the split file on '+ const)
            for i in result_new:
                slave_queue.append([job,i])
    

if __name__ == "__main__":
    const = '/mnt/volume-sgp1-01/origin/'
    const2 = '/mnt/volume-sgp1-01/proj/'
    proj_id = []
    slave_queue = []
    thread = threading.Thread(target=ffmpeg_call, args=())
    thread.daemon = True # Daemonize thread
    thread.start()
    main()