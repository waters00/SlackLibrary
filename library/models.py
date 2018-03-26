#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Reader(models.Model):
    class Meta:
        verbose_name = '读者'
        verbose_name_plural = '读者'

    user = models.OneToOneField(User)
    name = models.CharField(max_length=16, unique=True)
    phone = models.IntegerField(unique=True)
    max_borrowing = models.IntegerField(default=5)
    balance = models.FloatField(default=0.0)
    photo = models.ImageField(blank=True, upload_to='images/')

    STATUS_CHOICES = (
        (0, 'normal'),
        (-1, 'overdue')
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    class Meta:
        verbose_name = '图书'
        verbose_name_plural = '图书'

    ISBN = models.CharField(max_length=13, primary_key=True)
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=32)
    press = models.CharField(max_length=64)

    description = models.CharField(max_length=1024, default='')
    price = models.CharField(max_length=20, null=True)

    category = models.CharField(max_length=64, default=u'文学')
    cover = models.ImageField(null=True)
    index = models.CharField(max_length=16, null=True)
    location = models.CharField(max_length=64, default=u'图书馆1楼')
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.title + self.author


class Borrowing(models.Model):
    class Meta:
        verbose_name = '借阅'
        verbose_name_plural = '借阅'

    reader = models.ForeignKey(Reader)
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)
    date_issued = models.DateField()
    date_due_to_returned = models.DateField()
    date_returned = models.DateField(null=True)
    amount_of_fine = models.FloatField(default=0.0)

    def __str__(self):
        return '{} 借了 {}'.format(self.reader, self.ISBN)
