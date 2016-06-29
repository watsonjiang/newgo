#!/usr/bin/python
# -*- coding:utf-8 -*-
import newgo
newgo.init_logging()

from newgo import web
from newgo import model

model.init_db()

web.run_server()


