import tornado.ioloop
import tornado.web
import random
import secrets
import search
import time
import threading
import ffmpeg as ff

class utama(tornado.web.RequestHandler):
    def get(self):
        self.write("hello world")

class acak(tornado.web.RequestHandler):
    def get(self):
        ngacak = secrets.token_urlsafe(16)
        proj_id.append([ngacak,0,time.time()])
        ff.create_folder(const,ngacak)
        ff.create_folder(const+'proj/',ngacak)
        print(proj_id[len(proj_id)-1])
        self.write(str(ngacak))

class jobstart(tornado.web.RequestHandler):
    def get(self):
        var = self.get_argument('id')
        arr = proj_id
        dem = search.edit_stats(arr, var)
        if dem is True:
            search.queue_pass_array(var)#testing for queueing pending job
            print(var)
            self.write(str(var))
        else:
            print('Accessing to Unknown ID')
            self.write('Unknown ID')

class stats(tornado.web.RequestHandler):
    def get(self):
        var = self.get_argument('id')
        a, b = search.find(proj_id, var)
        if a is None:
            print('Accessing to Unknown ID')
            self.write('Unknown ID')
        else:
            var = str(a[1])
            count = str(b)
            print(var + count)
            self.write(var)
        

class slave_comm(tornado.web.RequestHandler):
    def get(self):
        pass

def main():
    application = tornado.web.Application([
        (r"/", utama),
        (r"/create", acak),
        (r"/start", jobstart),
        (r"/status", stats),
        (r"/slave", slave_comm)
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()

# Kode terpanjang dan terlama di program ini !
def ffmpeg_call():
    saat = True
    while saat is True:
        job = search.access_queue()#[proj_id, status, time] array structure
        if job is False:
            print('No job, time for sleeping for 10 second')
            time.sleep(10)
        else:
            result = str(search.search_file(const+str(job),"mp4"))
            print(result)
            ff.ffmpeg_call(const+job+'/'+result,job)
            print('success running ffmpeg project ' + str(job))
            result = search.search_file(const+'proj/'+str(job),"mp4")
            if not result:
                print('can\'t find the split file on '+ const) 
            for i in result:
                slave_queue.append([i,job[1]])
            print(slave_queue)

if __name__ == "__main__":
    const = '/mnt/volume-sgp1-01/'
    proj_id = []
    slave_queue = []
    thread = threading.Thread(target=ffmpeg_call, args=())
    thread.daemon = True # Daemonize thread
    thread.start()
    main()