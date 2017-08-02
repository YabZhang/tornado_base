# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqllite:///sample.db')
# engine = create_engine('mysql+pymysql://user:passwd@host/mydatebase?charset=utf8',
#                       encoding='utf8', echo=False)

Session = sessionmaker(bind=engine)
