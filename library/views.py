#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required

import json

from models import Book, Reader, User
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



