#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    author = Column(String)
    press = Column(String)
    ISBN = Column(String)
    cover = Column(String)
    price = Column(String)
    description = Column(Text)

    def __repr__(self):
        return self.title + ' ' + self.ISBN


def get_sqlalchemy_session():
    engine = create_engine('sqlite:///books.sqlite3')

    DB_session = sessionmaker()
    DB_session.configure(bind=engine)
    # Base.metadata.create_all(engine)

    session = DB_session()
    return session


session = get_sqlalchemy_session()

item = {}

item['title'] = 'x'
item['title'] = 'x'
item['author'] = 'x'
item['press'] = 'x'
item['ISBN'] = 'x'
item['cover'] = 'x'
item['price'] = 'x'
item['description'] = 'x'

book = Book(
    title=item['title'],
    author=item['author'],
    press=item['press'],
    ISBN=item['ISBN'],
    cover=item['cover'],
    price=item['price'],
    description=item['description'],
)
session.add(book)
session.commit()
