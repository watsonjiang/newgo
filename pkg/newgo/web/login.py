#!/usr/bin/python
# -*- coding:utf8 -*-

from webob import Response
import xhtml
import csv
import newgo
from newgo.web.req_dispatcher import Get, Post
from newgo import core


LOGGER = newgo.get_logger(newgo.LOG_MODULE_UI)

@Get('/login')
def get_login_view(req):
   rsp = Response()
   rsp.status_code = 200
   rsp.content_type = 'text/html'
   kw = {}
   if 'username' in req.session:
      kw['username'] = req.session['username']
   rsp.unicode_body = xhtml.render_page('login', kw)
   return rsp

@Post('/login')
def post_login_view(req):
   rsp = Response()
   username = req.POST['username']
   password = req.POST['password']
   try:
      core.auth_user(username, password)
   except:
      LOGGER.exception('Fail to auth user!')
      rsp.status_code = 200
      rsp.content_type = 'text/html'
      kw = {}
      kw['auth_error'] = "Name or password not correct!"   
      rsp.unicode_body = xhtml.render_page('login', kw)
      return rsp
   
   req.session['username'] = username
   rsp.status_code = 302
   rsp.location = '/home'
   return rsp

