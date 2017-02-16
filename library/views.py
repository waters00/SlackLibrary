#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

import json

from models import Book


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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponse(u'Your account is disabled.')
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'library/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
