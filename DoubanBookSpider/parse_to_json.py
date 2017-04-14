#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from DoubanBookSpider.pipelines import Book, get_sqlalchemy_session


def do():
    session = get_sqlalchemy_session()
    books = session.query(Book).all()
    with open('books.json', 'w') as f:
        book_list = []
        for book in books:
            _book = {}

            _book['title'] = book.title
            _book['author'] = book.author
            _book['press'] = book.press
            _book['ISBN'] = book.ISBN
            _book['cover'] = book.cover
            _book['price'] = book.price
            _book['description'] = book.description
            book_list.append(_book)

        f.write(json.dumps(book_list))


if __name__ == '__main__':
    do()
