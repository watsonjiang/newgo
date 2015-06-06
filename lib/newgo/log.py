#!/usr/bin/python
# -*- coding:utf8 -*-
import os
import os.path
import logging
import logging.config

LOG_MODULE_UI = 'webui'

_loggers = {
   LOG_MODULE_UI: logging.getLogger(LOG_MODULE_UI),
}

def init():
   NEWGO_HOME = os.getenv('NEWGO_HOME')
   cfname = os.path.join(NEWGO_HOME, 'conf/logging.conf')
   logging.config.fileConfig(cfname)

def getLogger(module):
   if module in _loggers.keys():
      return _loggers[module]   
   else:
      raise ValueError('%s is not valid log module.' % module)
