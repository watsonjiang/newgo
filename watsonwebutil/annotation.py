#!/bin/python
# -*- coding:utf-8 -*-

from webob import Request

def WebMethod(func):
    def replacement(environ, start_response):
        req = Request(environ)
        return func(req, **req.urlvars)
    return replacement