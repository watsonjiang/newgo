#!/usr/bin/python
# -*- coding:utf8 -*-
from webob import Request
from webob import Response
from newgo.webutil import ReqRouter
from wsgiref import simple_server
from newgo import log
import static


def _getRequestRouter():
    reqRouter = ReqRouter()
    reqRouter.add_route("/", "newgo.redirect_to_start_view")
    reqRouter.add_route("/home", "newgo.start_view")
    reqRouter.add_route("/login", "newgo.login_view")
    return reqRouter

def _app(environ, start_response):
    reqRouter = _getRequestRouter()
    req = Request(environ)
    if req.path_info.startswith("/static"):
        return static.static_file_handler(req.path_info)(environ, start_response)
    return reqRouter(environ, start_response)

logger = log.getLogger(log.LOG_MODULE_UI)

def run_server():
   server = simple_server.make_server("", 8080, _app)
   sa = server.socket.getsockname()
   logger.info("Serving HTTP on %s port %d ...", sa[0], sa[1])
   server.serve_forever()

if __name__ == "__main__":
   run_server()