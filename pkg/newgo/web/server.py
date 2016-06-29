#!/usr/bin/python
# -*- coding:utf8 -*-
'''
module to start wsgi server
'''
from wsgiref import simple_server
from webob import Request
import newgo
from newgo.web.req_dispatcher import ReqDispatcher
from newgo.web import static
from newgo.config import Config

#this 2 import to register web api
from newgo.web import start
from newgo.web import login

def _app(environ, start_response):
   req = Request(environ)
   if req.path_info.startswith("/static"):
      return static.static_file_handler(req.path_info)(environ, start_response)
   return ReqDispatcher()(environ, start_response)

LOGGER = newgo.get_logger(newgo.LOG_MODULE_UI)

def run_server():
   server = simple_server.make_server(Config().web_host(),
                                      Config().web_port(), _app)
   sa = server.socket.getsockname()
   LOGGER.info("Serving HTTP on %s port %d ...", sa[0], sa[1])
   server.serve_forever()
