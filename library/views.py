#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse
from django import forms


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


def login(request):
    context = {
        'a': 'a',
    }
    return render(request, 'library/login.html', context)
