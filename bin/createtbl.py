#!/usr/bin/env python

from newgo import model

if __name__ == "__main__":
#   model.create_schema()
    u = model.User()
    u.uid = 1
    u.name = 'watson'
    u.passwd = '123456'
