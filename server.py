import os
import time
from datetime import datetime
import json
import tornado.ioloop
import tornado.web
import tornado.options
from tornado import websocket
import psutil

tornado.options.enable_pretty_logging()


web_sockets = []


def get_process_dict():
    results = []
    me = os.getuid()
    for p in psutil.process_iter():
        if me == p.uids.real:
            cpu_time = p.get_cpu_times()
            results.append({
                'pid':              p.pid,
                'create_time':      datetime.fromtimestamp(p.create_time).strftime('%Y-%m-%d %H:%M'),
                'username':         p.username,
                'thread_count':     p.get_num_threads(),
                'rss':              p.get_memory_info().rss,
                'cpu':              time.strftime('%H:%M:%S', time.gmtime(cpu_time[0] + cpu_time[1])),
                'cmdline':          ' '.join(p.cmdline)
            })
    return results


class API_ProcessList(tornado.web.RequestHandler):
    def get(self):
        self.write({'results': get_process_dict()})


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
        start = datetime.utcnow()
        d = json.dumps({'results': get_process_dict()})
        for socket in web_sockets:
            socket.write_message(d)
        print (datetime.utcnow() - start).total_seconds()

if __name__ == '__main__':
    application.listen(8888)

    sched = tornado.ioloop.PeriodicCallback(update_processes, 2000)
    sched.start()

    tornado.ioloop.IOLoop.instance().start()
