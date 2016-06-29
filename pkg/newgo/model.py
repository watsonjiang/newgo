#!/usr/bin/env python
# -*- coding:utf8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import Integer, VARCHAR, Float
from sqlalchemy.types import DateTime
from sqlalchemy.orm import scoped_session, sessionmaker
from newgo.config import Config


Base = declarative_base()

Session = scoped_session(sessionmaker())

def init_db():
   from sqlalchemy import create_engine
   url = 'mysql+mysqldb://{user}:{passwd}@{host}:{port}/{dbname}' \
         .format(user=Config().db_user(),
                 passwd=Config().db_passwd(),
                 host=Config().db_host(),
                 port=Config().db_port(),
                 dbname=Config().db_name())
   engine = create_engine(url)
   Session.configure(bind=engine)
   

def create_schema():
   from sqlalchemy import create_engine
   url = 'mysql+mysqldb://{user}:{passwd}@{host}:{port}/{dbname}' \
         .format(user=Config().db_user(),
                 passwd=Config().db_passwd(),
                 host=Config().db_host(),
                 port=Config().db_port(),
                 dbname=Config().db_name())
   engine = create_engine(url)
   Base.metadata.create_all(bind=engine)


class User(Base):
   __tablename__ = 'uinfo'

   uid = Column('id', Integer, primary_key=True) 
   name = Column('name', VARCHAR(255))
   passwd = Column('cred', VARCHAR(255))

   def __repr__(self):
      return "User[{uid}, {name}, {passwd}]".format(**self.__dict__)


class Menu(Base):
   __tablename__ = 'menu'

   mid = Column('id', Integer, primary_key=True)
   name = Column('name', VARCHAR(255))

class Order(Base):
   __tablename__ = 'order'

   uid = Column('uid', Integer, ForeignKey(User.uid),
                primary_key=True)
   mid = Column('mid', Integer, ForeignKey(Menu.mid),
                primary_key=True)
   payment = Column('payment', Float)
   time = Column('date', DateTime) 




