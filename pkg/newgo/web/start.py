#!/usr/bin/python
# -*- coding: utf-8 -*-

import os.path
import codecs
import datetime
import xhtml
from webob import Response
from newgo.webutil import UnicodeCsvReader
from newgo.webutil import UnicodeCsvWriter
import newgo
from newgo.web.req_dispatcher import Get

logger = newgo.get_logger(newgo.LOG_MODULE_UI)

def check_file_exist(fname):
   if not os.path.exists(fname):
      with open(fname, 'w') as f:   # create an empty file
         pass

def get_menu():
   m = []
   return ["item1", "item2"]
   with codecs.open('menu.txt', 'r', 'utf-8') as f:
      for s in f:
         m.append(s)
   return m

#order record format:  user,food,price,date   
def get_order_list():
   m = []
   fname = "".join(['order', '.', datetime.date.today().isoformat()])
   check_file_exist(fname)   
   with open(fname, 'r') as f:
      reader = UnicodeCsvReader(f)
      for row in reader:
         m.append(row)
   return m

def new_order(user, food_index):
   fname = 'menu.txt'
   food_name = None
   food_price = 0
   check_file_exist(fname)
   with open(fname, 'r') as f:
      reader = UnicodeCsvReader(f)
      index = 0
      for row in reader:
         if food_index == index:
            food_name = row[0]
            food_price = row[1]
            break
         index = index + 1

   if food_name is None:
      logger.warning("No food found (index %d). ignore this order.", food_index)
      return
   
   fname = ''.join(['order', '.', datetime.date.today().isoformat()])
   check_file_exist(fname)
   with open(fname, 'a') as f:
      writer = UnicodeCsvWriter(f)
      writer.writerow([user, food_name, food_price, datetime.date.today().isoformat()])

def cancel_order(order_index):
   fname = ''.join(['order', '.', datetime.date.today().isoformat()])
   tmp = []
   check_file_exist(fname)
   with open(fname, 'r') as f:
      reader = UnicodeCsvReader(f)
      for row in reader:
         tmp.append(row)

   with open(fname, 'w') as f:
      writer = UnicodeCsvWriter(f)
      index = 0
      for row in tmp:
         if index == order_index:
            index = index + 1
            continue
      writer.writerow(row)
      index = index + 1

@Get('/')
@Get('/home')
def start_view(req):
   rsp = Response()
   rsp.status_code = 200
   rsp.content_type = 'text/html'
   kw = {'menu':get_menu(),
         'order_list':get_order_list(),  
         'today':datetime.date.today().isoformat()
        }
   if 'username' in req.session:
      kw['username'] = req.session['username']
   rsp.unicode_body = xhtml.render_page('start', kw)
   return rsp 
