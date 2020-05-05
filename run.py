# coding=utf-8
# __author__ = 'Mio'

import logging

from tornado.options import parse_command_line, define, options
import tornado.ioloop
import tornado.web

from handler import conn_gotify
from settings import loop, async_loop

define("port", default=8080, help="Worker run on the given port", type=int)
define("debug", default=False, help="run in debug mode")
parse_command_line()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


def make_app():
    return tornado.web.Application()


if __name__ == "__main__":
    app = make_app()
    app.listen(options.port)

    async_loop.create_task(conn_gotify())

    logging.info(f"App run on: http://localhost:{options.port}")
    loop.start()
