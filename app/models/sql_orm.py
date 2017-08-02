# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String, server_default=Text(''))
    fullname = Column(String, server_default=Text(''))
    email = Column(String, server_default=Text(''))
    password = Column(String, server_default=Text(''))

    def __repr__(self):
        return "<User(id=%s, name=%s)>" % (self.id, self.name)
