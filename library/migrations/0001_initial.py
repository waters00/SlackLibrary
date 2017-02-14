# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('ISBN', models.CharField(max_length=13, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('author', models.CharField(max_length=32)),
                ('press', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='BookInfo',
            fields=[
                ('ISBN', models.CharField(max_length=13, serialize=False, primary_key=True)),
                ('description', models.CharField(max_length=1024)),
                ('price', models.FloatField()),
                ('category', models.CharField(max_length=64)),
                ('cover', models.ImageField(upload_to=b'')),
                ('index', models.CharField(max_length=16)),
                ('location', models.CharField(max_length=64)),
                ('quantity', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Borrowing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_issued', models.DateField()),
                ('date_due_to_returned', models.DateField()),
                ('date_returned', models.DateField()),
                ('amount_of_fine', models.FloatField(default=0.0)),
                ('ISBN', models.ForeignKey(to='library.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Reader',
            fields=[
                ('ID', models.IntegerField(serialize=False, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=16)),
                ('phone', models.IntegerField()),
                ('max_borrowing', models.IntegerField(default=5)),
                ('balance', models.FloatField(default=0.0)),
                ('status', models.IntegerField(default=-1, choices=[(0, b'normal'), (-1, b'overdue')])),
            ],
        ),
        migrations.AddField(
            model_name='borrowing',
            name='reader_id',
            field=models.ForeignKey(to='library.Reader'),
        ),
        migrations.AddField(
            model_name='book',
            name='info',
            field=models.OneToOneField(to='library.BookInfo'),
        ),
    ]
