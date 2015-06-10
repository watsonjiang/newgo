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
   cfname = os.path.join(NEWGO_HOME, 'conf/logging.conf')
   logging.config.fileConfig(cfname)

def getLogger(module):
   if module in _loggers.keys():
      return _loggers[module]   
   else:
      raise ValueError('%s is not valid log module.' % module)
