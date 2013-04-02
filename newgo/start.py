#!/usr/bin/python
# -*- coding: utf-8 -*-

from webob import Request
from webob import Response
from watsonwebutil import WebMethod
import datetime
from pageloader import load_page
import logging
import codecs
from watsonwebutil import UnicodeCsvReader
from watsonwebutil import UnicodeCsvWriter
import os.path

logger = logging.getLogger("newgo")
    
def check_file_exist(fname):
    if not os.path.exists(fname):
      with open(fname, 'w') as f:    # create an empty file
        pass    
    
def get_menu():
    m = []
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
          
    if None == food_name:
      logger.warning("No food found (index %d). ignore this order." % food_index )
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
    
@WebMethod
def redirect_to_start_view(req):
    rsp = Response()
    rsp.status_code = 302
    rsp.location = "/home"
    return rsp

def start_view_get(req):
    rsp = Response()
    rsp.status_code = 200
    rsp.content_type = 'text/html'
    kw = {
          'menu':get_menu(),
          'order_list':get_order_list(),  
          'today':datetime.date.today().isoformat()
         }
    if 'username' in req.session:
      kw['username'] = req.session['username']
    rsp.unicode_body = load_page('start')(**kw)
    return rsp 

def start_view_post(req):
    if not 'username' in req.session:
      rsp = Response()
      rsp.status_code = 404
      return rsp      

    if req.POST['operation'] == 'new_order':
      new_order(req.session['username'], int(req.POST['food_index']))
    elif req.POST['operation'] == 'cancel_order':
      cancel_order(int(req.POST['order_index']))
    rsp = Response()
    rsp.status_code = 302
    rsp.location = "/home"
    return rsp
    
    
@WebMethod
def start_view(req): 
    if req.method.lower() == 'get':
      return start_view_get(req)
    else:
      return start_view_post(req)