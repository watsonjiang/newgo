#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from chameleon import PageTemplateLoader

def load_page(name):
   path = os.path.dirname(__file__)
   loader = PageTemplateLoader(path, '.xhtml')
   return loader[name]
