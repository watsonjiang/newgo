#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os
from webob.static import FileApp
import newgo

logger = newgo.get_logger(newgo.LOG_MODULE_UI)

def static_file_handler(file_path):
   fname = os.path.basename(file_path)
   path = os.path.dirname(__file__)+ os.sep + fname
   logger.debug("Retrive static file %s", path)
   return FileApp(path); 
