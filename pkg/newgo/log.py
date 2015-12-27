#!/usr/bin/python
# -*- coding:utf8 -*-
import os
import os.path
import logging
import logging.config

LOG_MODULE_ROOT = 'newgo'
LOG_MODULE_UI = 'newgo.webui'
LOG_MODULE_DATASTORE = 'newgo.datastore'

_loggers = {
   LOG_MODULE_ROOT: logging.getLogger(LOG_MODULE_ROOT),
   LOG_MODULE_UI: logging.getLogger(LOG_MODULE_UI),
   LOG_MODULE_DATASTORE: logging.getLogger(LOG_MODULE_DATASTORE),
}

def init_logging():
   NEWGO_HOME = os.getenv('NEWGO_HOME')
   if not NEWGO_HOME:
      raise ValueError('NEWGO_HOME is empty')
   cf_name = os.path.join(NEWGO_HOME, 'conf/logging.conf')
   logging.config.fileConfig(cf_name)

def get_logger(name):
   return logging.getLogger(name)
