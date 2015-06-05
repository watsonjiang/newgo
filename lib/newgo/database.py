#!/usr/bin/python
# -*- coding:utf-8 -*-

import shelve
from datetime import date

logger = logging.getLogger("newgo.database")

class OrderRecords(object):
"""The class to persist order list."""
    def _getDbFileName():
        today = date.today()
        return 'order_%d_%d_%d' % (today.year, today.month, today.day)
    
    def getTodayOrderList(self):
        """Return the order list of today. """
        file_name = _getDbFileName()
        db = shelve.open(file_name)
        rst = db['order_list']
        db.close()
       
    def updateOrderList(self, orderList):
        """Write the order list into today's order list file.""" 
        file_name = _getDbFileName()
        db = shelve.open(file_name)
        db['order_list'] = orderList
        db.close()
        
        