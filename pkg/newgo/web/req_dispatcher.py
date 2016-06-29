#!/bin/python
# -*- coding:utf-8 -*-

import re
import sys
import traceback
import uuid
from webob import Request
from webob import Response
from webob import exc
import newgo
from newgo.singleton import Singleton

CONST_STR_SESSIONID = 'sessionid'

LOGGER = newgo.get_logger(newgo.LOG_MODULE_UI)

session_repo = {}

class Get(object):
   def __init__(self, path):
      self.path = path

   def __call__(self, func):
      ReqDispatcher().add_route('GET', self.path, func)
      return func

class Post(object):
   def __init__(self, path):
      self.path = path

   def __call__(self, func):
      ReqDispatcher().add_route('POST', self.path, func)
      return func

def _template_to_regex(template):
   regex = ''
   last_pos = 0
   for match in ReqDispatcher.VAR_REGEX.finditer(template):
      regex += re.escape(template[last_pos:match.start()])
      var_name = match.group(1)
      expr = match.group(2) or '[^/]+'
      expr = '(?P<%s>%s)' % (var_name, expr)
      regex += expr
      last_pos = match.end()
   regex += re.escape(template[last_pos:])
   regex = '^%s$' % regex
   return regex


def _load_handler(string):
   module_name, func_name = string.split('.', 1)
   __import__(module_name)
   module = sys.modules[module_name]
   handler = getattr(module, func_name)
   return handler 	


class ReqDispatcher(object):
   
   __metaclass__ = Singleton

   ALLOWED_METHODS = set(['get', 'post', 'put', 'head', 'delete'])
   VAR_REGEX = re.compile(r'''
     \{            # The exact character "{"
     (\w+)         # The variable name (restricted to a-z, 0-9, _)
     (?::([^}]+))? # The optional :regex part
     \}            # The exact character "}"
     ''', re.VERBOSE)

   def __init__(self):
      self.routes = []

   def add_route(self, method, template, handler, **kwargs):
      if isinstance(handler, basestring):
         handler = _load_handler(handler)
      self.routes.append((method, re.compile(_template_to_regex(template)),
                         handler, kwargs))

   def load_session(self, sid):
      if sid in session_repo:
         return session_repo[sid]
      else:
         return {}

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
         for method, regex, handler, kwargs in self.routes:
            match = regex.match(req.path_info)
            if match:
               if method == '*' or req.method.upper() == method:
                  req.urlvars = match.groupdict()
                  req.urlvars.update(kwargs)
                  resp = handler(req, **req.urlvars)
                  if isinstance(resp, Response):
                     if len(req.session) > 0:    #require session data 
                        req.sessionid = uuid.uuid4().hex
                        resp.set_cookie(CONST_STR_SESSIONID, req.sessionid)
                        self.save_session(req.sessionid, req.session)
                     return resp(environ, start_response)
                  else:
                     raise exc.HTTPInternalServerError(detail='no response')
         return exc.HTTPNotFound()(environ, start_response)
      except exc.WSGIHTTPException as ex:
         return ex(environ, start_response)
      except:
         LOGGER.exception("Unexpected exception!")
         lines = ''.join(traceback.format_exception(*sys.exc_info()))
         return exc.HTTPInternalServerError(detail='%s' % lines)
