#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json

from models import Book, Reader, User, Borrowing
from forms import PhotoForm


class aForm(forms.Form):
    your_name = forms.CharField(label=u'请输入书名/ISBN/作者名', max_length=100)


def index(request):
    if request.method == 'POST':
        form = aForm(request.POST)
        if form.is_valid():
            return HttpResponse(u'书不存在')
    else:
        form = aForm()

    context = {
        'form': form,
    }
    return render(request, 'library/index.html', context)


def user_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user:
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse(u'Your account is disabled.')
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'library/login.html', {})


def user_register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    state = None
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if password == '' or repeat_password == '':
            state = 'empty'
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            username = request.POST.get('username', '')
            name = request.POST.get('name', '')
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create(username=username)
                new_user.save()
                new_reader = Reader.objects.create(user=new_user, name=name, phone=int(username))
                new_reader.photo = request.FILES['photo']
                new_reader.save()
                state = 'success'

                auth.login(request, new_user)
                # return HttpResponseRedirect('/')

                context = {
                    'state': state,
                    'form': form,
                }
                return render(request, 'library/register.html', context)

    form = PhotoForm()

    context = {
        'state': state,
        'form': form,
    }

    return render(request, 'library/register.html', context)


@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')

        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'

    return render(request, 'library/set_password.html', {'state': state})


@login_required
def user_logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def profile(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login')

    id = request.user.id
    try:
        reader = Reader.objects.get(user_id=id)
    except Reader.DoesNotExist:
        return HttpResponse('no this id book')

    borrowing = Borrowing.objects.filter(reader=reader).all()

    context = {
        'reader': reader,
        'borrowing': borrowing,
    }
    return render(request, 'library/profile.html', context)


def book_search(request):
    search_by = request.GET.get('search_by', '书名')
    books = []
    current_path = request.get_full_path()

    keyword = request.GET.get('keyword', None)
    if not keyword:
        return HttpResponseRedirect('/')

    if search_by == u'书名':
        keyword = request.GET.get('keyword', None)
        books = Book.objects.filter(title__contains=keyword).order_by('-title')[0:50]
    elif search_by == u'ISBN':
        keyword = request.GET.get('keyword', None)
        books = Book.objects.filter(ISBN__contains=keyword).order_by('-title')[0:50]
    elif search_by == u'作者':
        keyword = request.GET.get('keyword', None)
        books = Book.objects.filter(author__contains=keyword).order_by('-title')[0:50]

    paginator = Paginator(books, 5)
    page = request.GET.get('page', 1)

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    print current_path

    context = {
        'books': books,
        'search_by': search_by,
        'keyword': keyword,
        'current_path': current_path,
    }
    return render(request, 'library/search.html', context)


def book_detail(request):
    ISBN = request.GET.get('ISBN', None)
    print ISBN
    if not ISBN:
        return HttpResponse('there is no such an ISBN')
    try:
        book = Book.objects.get(pk=ISBN)
    except Book.DoesNotExist:
        return HttpResponse('there is no such an ISBN')

    action = request.GET.get('action', None)
    state = None

    if action == 'borrow':

        if not request.user.is_authenticated():
            state = 'no_user'
        else:
            reader = Reader.objects.get(user_id=request.user.id)
            if reader.max_borrowing > 0:
                reader.max_borrowing -= 1
                reader.save()

                isbn = Book.objects.get(pk=ISBN)
                issued = datetime.date.today()
                due_to_returned = issued + datetime.timedelta(30)

                b = Borrowing.objects.create(
                    reader=reader,
                    ISBN=isbn,
                    date_issued=issued,
                    date_due_to_returned=due_to_returned)

                b.save()
                state = 'success'
            else:
                state = 'upper_limit'

    context = {
        'state': state,
        'book': book,
    }
    return render(request, 'library/book_detail.html', context)
