from src.main import *
from tornado.ioloop import IOLoop

if __name__ == '__main__':
    app = make_app()
    app.listen(3000)
    IOLoop.instance().start()