#!/usr/bin/python
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()

class Person(Base):
   __tablename__ = 'person'
   id = Column(Integer, primary_key=True)
   name = Column(String(20), nullable=False)

class Address(Base):
   __tablename__ = 'address'
   id = Column(Integer, primary_key=True)
   street_name = Column(String(20))
   street_number = Column(String(250))
   post_code = Column(String(250), nullable=False)
   person_id = Column(Integer, ForeignKey('person.id'))
   person = relationship(Person)

def create_store():
   engine = create_engine('sqlite:///newgo.db')
   Base.metadata.create_all(engine)

def insert_data():
   engine = create_engine('sqlite:///newgo.db')
   Base.metadata.bind = engine  
   DBSession = sessionmaker(bind=engine)
   session = DBSession()
   new_person = Person(name='new person')
   session.add(new_person)
   session.commit()

   new_address = Address(post_code='0000', person=new_person)
   session.add(new_address)
   session.commit() 

def query_data():
   engine = create_engine('sqlite:///newgo.db')
   Base.metadata.bind = engine  
   DBSession = sessionmaker(bind=engine)
   session = DBSession()
   persons = session.query(Person).all()
   for p in persons:
      print p.name 

def query_data1():
   import sqlite3
   conn = sqlite3.connect('newgo.db')
   c = conn.cursor()
   c.execute('select * from address')
   print c.fetchall()
   c.execute('select * from person')
   print c.fetchall()


if __name__ == "__main__":
   create_store() 
   insert_data()
   query_data()
   query_data1()
