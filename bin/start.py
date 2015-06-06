#!/usr/bin/python
# -*- coding:utf-8 -*-

from newgo import run_server
import logging
import logging.config
import os
import os.path

NEWGO_HOME = os.getenv('NEWGO_HOME')

cf_name = os.path.join(NEWGO_HOME, 'conf/logging.conf')
logging.config.fileConfig(cf_name)

run_server()
