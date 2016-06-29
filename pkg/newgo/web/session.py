#!/usr/bin/env python
# -*- coding:utf8 -*-
import threading


class Session(object):
   sess_obj = threading.local()

   @staticmethod
   def get_session():
      sess_obj.id = 123

   def __getter__():
      pass

   def __setter__():


