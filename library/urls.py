#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.user_login, name='user_login'),
    url(r'^logout/', views.user_logout, name='user_logout')
]
