#!/usr/bin/env python
# -*- coding:utf8 -*-

import ConfigParser
from newgo.singleton import Singleton
from os.path import join
import os

class Config(object):
 
   __metaclass__ = Singleton

   conf = ConfigParser.ConfigParser()
   
   def __init__(self):
      home = os.getenv('NEWGO_HOME')
      path = join(home, 'conf', 'newgo.conf')
      Config.conf.read(path)

   def db_host(self):
      return self.conf.get('db', 'host')

   def db_port(self):
      return self.conf.getint('db', 'port')

   def db_name(self):
      return self.conf.get('db', 'dbname')

   def db_user(self):
      return self.conf.get('db', 'user')

   def db_passwd(self):
      return self.conf.get('db', 'passwd')

   def web_host(self):
      return self.conf.get('web', 'host')

   def web_port(self):
      return self.conf.getint('web', 'port')
