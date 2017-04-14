#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Slackers.settings')

import django

django.setup()

import json
import random
import datetime
import os.path as op
from library.models import Book, Reader, Borrowing
from django.contrib.auth.models import User

from faker import Factory

fake = Factory.create('zh_CN')


def init_reader_data(amount=50):
    for i in range(amount):
        u = User.objects.get_or_create(username=fake.phone_number())[0]
        u.set_password('password')
        u.save()

        r = Reader.objects.get_or_create(user=u, name=fake.name(), phone=int(u.username))[0]
        r.balance = round(random.random() * 100, 2)
        r.photo = 'images/' + str(r.user_id) + '.jpg'
        r.save()


def init_book_data():
    with open(op.join('DoubanBookSpider', 'books.json'), 'r') as f:
        books = json.loads(f.read())

    for b in books:
        if b['description']:
            B = Book.objects.get_or_create(ISBN=b['ISBN'], title=b['title'], author=b['author'], press=b['press'])[0]
            B.description = b['description']
            B.price = b['price']
            B.cover = b['cover']
            B.quantity = random.randint(0, 7)
            B.save()


def init_borrowing_data(amount=50):
    for i in range(amount):
        try:
            reader = Reader.objects.get(pk=random.randint(1, 50))
        except Reader.DoesNotExist:
            pass
        isbn = random.choice(Book.objects.all())
        issued = datetime.date.today() + datetime.timedelta(random.randint(1, 30))
        due_to_returned = issued + datetime.timedelta(30)

        if reader.max_borrowing > 0:
            b = Borrowing.objects.create(
                reader=reader,
                ISBN=isbn,
                date_issued=issued,
                date_due_to_returned=due_to_returned)

            reader.max_borrowing -= 1
            reader.save()
            b.save()


if __name__ == '__main__':
    init_reader_data()
    init_book_data()
    init_borrowing_data()
