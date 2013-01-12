import os
import tornado.ioloop
import tornado.web
import tornado.options

tornado.options.enable_pretty_logging()

settings = {
    'debug': True,
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
}

application = tornado.web.Application([
    (r'/(.*\.html)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), 'app')})
], **settings)

if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
