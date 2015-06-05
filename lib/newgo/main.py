import re
import sys
import os
import traceback
import logging
from webob import Request
from webob import Response
from webob import exc
from watsonwebutil import ReqRouter
from wsgiref.simple_server import make_server
from static import static_file_handler


def getRequestRouter():
    reqRouter = ReqRouter()
    reqRouter.add_route("/", "newgo.redirect_to_start_view")
    reqRouter.add_route("/home", "newgo.start_view")
    reqRouter.add_route("/login", "newgo.login_view")
    return reqRouter
    

def app(environ, start_response):
    reqRouter = getRequestRouter()
    req = Request(environ)
    if req.path_info.startswith("/static"):
        return static_file_handler(req.path_info)(environ, start_response)
    return reqRouter(environ, start_response)

logger = logging.getLogger("newgo")
logging.basicConfig(level=logging.DEBUG)	
cwd = os.getcwd()
sys.path.insert(0, cwd)     #add / as package search path.

server = make_server("", 8080, app)
sa = server.socket.getsockname()
logger.info("Serving HTTP on %s port %d ...", sa[0], sa[1])
server.serve_forever()
