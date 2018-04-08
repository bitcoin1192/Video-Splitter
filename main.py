import time
import sqlite3 as db
import random
import os
import search
from flask import Flask, request, jsonify


app = Flask(__name__)

jobid = []
#status = False

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/create')
def create_folder():
    couint = 0
    state = True
    while state == True:#becareful infinite loop
        name = random_gen()
        if search.db_search(str(name)) is False:
            state = False
            search.db_insert(str(name))
            #c.execute('INSERT INTO record VALUES (?,0)', name)
        couint = couint + 1
        if couint > 10:#break loop incase of infinite loop
            return 'maybe we are out of name'
    #c.execute('INSERT INTO record VALUES (?,0)', name)
    print(name)
    #os.makedirs(name, mode=0o777, exist_ok=False)//please remove on production !
    return jsonify(nama=name)

@app.route('/start', methods=['GET', 'POST'])
def start_jobid():
    req = request.args.get('jobid')
    arr = search.db_search(req)
    #if search.search_nested(req, jobid) is True:
    if arr is not None:
        print('its there')
        return 'okay got it'
    else:
        #position = jobid.index(req)
        #jobid[position][1].append(1)
        #debug
        return 'wot'

@app.route('/status', methods=['GET', 'POST'])
def get_status():
    req = request.args.get('jobid')
    arr = search.db_search(str(req))
    if search.db_search(req) is not False:
        return arr
    else:
        return 'wot'

def random_gen():
    name = ''.join(random.choice('0123456789AaBbCcDdEeFf') for i in range(16))
    return name

def start_up():
    global c
    try:
        conn = db.connect('maindb', check_same_thread= False)
        c = conn.cursor()
        dem = c.execute('SELECT * FROM record')
        test = dem.fetchone()
        conn.close()
        #for row in test.keys:
        #    if row is None:
        #        c.execute('CREATE TABLE record (id text PRIMARY KEY, stats INT)')
        #    else: 
        #        return
    except conn.Error as e:
        print (e)
        c.execute('CREATE TABLE "record" ( "id" INTEGER PRIMARY KEY AUTOINCREMENT,"jobid" TEXT NOT NULL,"status" INTEGER NOT NULL)')
        conn.commit()
        conn.close()
        return start_up()
        time.sleep(10000)
    
start_up()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')