#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from chameleon import PageTemplateLoader

def render_page(name, kw):
   path = os.path.dirname(__file__)
   loader = PageTemplateLoader(path, '.xhtml')
   return loader[name](**kw)
