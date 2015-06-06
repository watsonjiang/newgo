#!/bin/python
# -*- coding:utf-8 -*-

import re
import sys
import traceback
import uuid
import csv
import pickle
from webob import Request
from webob import Response
from webob import exc
from newgo import log

CONST_STR_SESSIONID = 'sessionid'

logger = log.getLogger(log.LOG_MODULE_UI)

session_repo = {}

class ReqRouter(object):
  
  ALLOWED_METHODS = set(['get', 'post', 'put', 'head', 'delete'])
  routes = []
  VAR_REGEX = re.compile(r'''
     \{            # The exact character "{"
     (\w+)         # The variable name (restricted to a-z, 0-9, _)
     (?::([^}]+))? # The optional :regex part
     \}            # The exact character "}"
     ''', re.VERBOSE)
  
  def __init__(self):
    self.routes = []
	
  def load_handler(self, string):
    module_name, func_name = string.split('.', 1)
    __import__(module_name)
    module = sys.modules[module_name]
    handler = getattr(module, func_name)
    return handler 	
	
  def add_route(self, template, handler, **vars):
    if isinstance(handler, basestring):
       handler = self.load_handler(handler)
    self.routes.append((re.compile(self.template_to_regex(template)), handler, vars))
  
  def template_to_regex(self, template):
    regex = ''
    last_pos = 0
    for match in self.VAR_REGEX.finditer(template):
        regex += re.escape(template[last_pos:match.start()])
        var_name = match.group(1)
        expr = match.group(2) or '[^/]+'
        expr = '(?P<%s>%s)' % (var_name, expr)
        regex += expr
        last_pos = match.end()
    regex += re.escape(template[last_pos:])
    regex = '^%s$' % regex
    return regex	
  
#  def load_session(self, sid):
#    with open('session.txt', 'r+') as f:
#      reader = csv.reader(f)
#      for kw in reader:
#        if sid == kw[0]:
#          return pickle.loads(kw[1])
#    return {}
  def load_session(self, sid):
    if sid in session_repo:
      return session_repo[sid]
    else:
      return {}      
          
#  def save_session(self, sid, session):
#    tmp = pickle.dumps(session)
#    with open('session.txt', 'a+') as f:
#      writer = csv.writer(f)
#      writer.writerow([sid, tmp])
  def save_session(self, sid, session):
    session_repo[sid] = session
  
  def __call__(self, environ, start_response):
    req = Request(environ)
    #set the session id
    if CONST_STR_SESSIONID in req.cookies:  #session exit
      req.sessionid = req.cookies['sessionid']
      req.session = self.load_session(req.sessionid)
    else:
      req.sessionid = None
      req.session = {}      
    try:
      for regex, handler, vars in self.routes:
         match = regex.match(req.path_info)
         if match:
            req.urlvars = match.groupdict()
            req.urlvars.update(vars)
            resp = handler(environ, start_response)
            if isinstance(resp, Response):
              if len(req.session) > 0:    #require session data 
                req.sessionid = uuid.uuid4().hex
                resp.set_cookie(CONST_STR_SESSIONID, req.sessionid)
                self.save_session(req.sessionid, req.session)
            return resp(environ, start_response)
      return exc.HTTPNotFound()(environ, start_response)
    except exc.WSGIHTTPException, ex:
      return ex(environ, start_response)
    except Exception, ex:
      return self.handle_exception(ex)(environ, start_response)
	  	
  def handle_exception(self, ex):
    logging.exception("Unhandled exception")
    lines = ''.join(traceback.format_exception(*sys.exc_info()))
    return exc.HTTPInternalServerError(detail='%s' % lines)	
	
  def head(self, **kwargs):
    method = getattr(self, 'get', None)
    if not method:
      raise webob.exc.HTTPMethodNotAllowed()
    method(**kwargs)
    self.response.body = ''	
