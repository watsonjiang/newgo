#!/usr/bin/python
# -*- coding:utf8 -*-

from webob import Response
import xhtml
import csv
import newgo
from newgo.web.req_dispatcher import Get


logger = newgo.get_logger(newgo.LOG_MODULE_UI)

def get_login_view(req):
   rsp = Response()
   rsp.status_code = 200
   rsp.content_type = 'text/html'
   kw = {}
   if 'username' in req.session:
      kw['username'] = req.session['username']
   rsp.unicode_body = xhtml.render_page('login', kw)
   return rsp

def post_login_view(req):
   rsp = Response()
   username = req.POST['username']
   password = req.POST['password']
   auth_error = None
   with open('passwd.txt') as f:
      reader = csv.reader(f)
      for u in reader:
         if u[0] == username and u[1] == password:
            req.session['username'] = username
            rsp.status_code = 302
            rsp.location = '/home'
            return rsp

   rsp.status_code = 200
   rsp.content_type = 'text/html'
   kw = {}
   kw['auth_error'] = "Name or password not correct!"   
   rsp.unicode_body = xhtml.render_page('login', kw)
   return rsp


@Get('/login')
def login_view(req):
   if req.method.lower() == 'post':
      return  post_login_view(req)
   else:
      return  get_login_view(req)

