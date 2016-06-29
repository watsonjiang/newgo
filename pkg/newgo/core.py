#!/usr/bin/env python
# -*- coding:utf8 -*-
import logging
import newgo
from newgo.model import *


LOGGER = newgo.get_logger(newgo.LOG_MODULE_DATASTORE)

def _transactional(func):
   def __wrapper(*args, **kwargs):
      try:
         func(*args, **kwargs)
         Session().commit()
      except:
         Session().rollback()
      finally:
         Session.remove()
   return __wrapper

def get_user(name):
   Session().query(User). \
             filter(User.name==name).first()

def get_menu():
   pass

def get_order_today():
   pass

@_transactional
def auth_user(name, passwd):
   u = get_user(name)
   LOGGER.debug("11111111%s %s", u.passwd, password)
   if u.passwd != password:
      raise ValueError('Invalid username or password') 


@_transactional
def add_user(name, passwd):
   u = User()
   u.uid = 0
   u.name = name
   u.passwd = passwd
   Session().add(u)

