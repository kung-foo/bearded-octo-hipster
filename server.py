#!/usr/bin/env python
import os
import time
from datetime import datetime
import json
import tornado.ioloop
import tornado.web
import tornado.options
from tornado import websocket
import psutil
import hashlib
from collections import OrderedDict

tornado.options.enable_pretty_logging()

web_sockets = []
process_map = {}


def get_process_map():
    results = {}
    me = os.getuid()
    for p in psutil.process_iter():
        if me == p.uids.real:
            proc_hash = '%d:%d' % (p.pid, p.create_time)
            proc_hash = hashlib.md5(proc_hash).hexdigest()
            cpu_time = time.gmtime(reduce(lambda x, y: x + y, p.get_cpu_times()))
            row = OrderedDict()
            row['pid'] = p.pid
            row['create_time'] = datetime.fromtimestamp(p.create_time).strftime('%Y-%m-%d %H:%M')
            row['username'] = p.username
            row['thread_count'] = p.get_num_threads()
            row['rss'] = p.get_memory_info().rss
            row['cpu_time'] = time.strftime('%H:%M:%S', cpu_time)
            #row['cpu_pct'] = p.get_cpu_percent(interval=0.01)
            row['cmdline'] = ' '.join(p.cmdline)
            row['proc_hash'] = proc_hash
            row['sep'] = os.path.sep
            results[proc_hash] = row
    return results


def hash_row(row):
    m = hashlib.md5()
    [m.update(str(f)) for f in row.values()]
    return m.hexdigest()


class API_ProcessList(tornado.web.RequestHandler):
    def get(self):
        self.write({'records': get_process_map().values()})


class WSAPI_ProcessList(websocket.WebSocketHandler):
    def open(self):
        web_sockets.append(self)

    def on_close(self):
        web_sockets.remove(self)

settings = {
    'debug': True,
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
}

application = tornado.web.Application([
    (r"/wsapi/process_list", WSAPI_ProcessList),
    (r'/api/process_list', API_ProcessList),
    (r'/(.*\.html)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'app')})
], **settings)


def update_processes():
    if web_sockets:
        new_process_map = get_process_map()
        added = set(new_process_map.keys()) - set(process_map.keys())
        removed = set(process_map.keys()) - set(new_process_map.keys())
        updated = set()

        results = {}
        results['records'] = {}

        for k in added:
            process_map[k] = new_process_map[k]
            results['records'][k] = new_process_map[k]

        for k in removed:
            del process_map[k]

        for k in process_map:
            if hash_row(process_map[k]) != hash_row(new_process_map[k]):
                updated.add(k)
                process_map[k] = new_process_map[k]
                results['records'][k] = new_process_map[k]

        print 'added:', len(added), 'removed:', len(removed), 'updated:', len(updated)

        results['updated'] = list(updated)
        results['added'] = list(added)
        results['removed'] = list(removed)

        d = json.dumps(results)
        print 'sending %d bytes' % len(d)
        for socket in web_sockets:
            socket.write_message(d)

if __name__ == '__main__':
    application.listen(8888)

    sched = tornado.ioloop.PeriodicCallback(update_processes, 1000)
    sched.start()

    tornado.ioloop.IOLoop.instance().start()
