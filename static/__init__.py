#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
import os
from webob import Request
from webob import Response
from webob.static import FileApp
from watsonwebutil import WebMethod
import os.path

BASE_DIR='.'
logger=logging.getLogger("newgo.static")

def static_file_handler(file_path):
    path = os.path.join(BASE_DIR, file_path[1:])
    logger.debug("Retrive static file %s", path)
    return FileApp(path); 
