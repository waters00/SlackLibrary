# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



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
    description = Column(String)

    def __repr__(self):
        return self.title + ' ' + self.ISBN


def get_sqlalchemy_session():
    engine = create_engine('sqlite:///books.sqlite3')

    DB_session = sessionmaker()
    DB_session.configure(bind=engine)
    # Base.metadata.create_all(engine)

    session = DB_session()
    return session


class DoubanbookPipeline(object):
    def process_item(self, item, spider):
        session = get_sqlalchemy_session()

        is_exist = session.query(Book).filter_by(ISBN=item['ISBN']).all()

        if not is_exist:
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

        return item
