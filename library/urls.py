#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.contrib.staticfiles import views as static_views
from django.conf.urls.static import static
from django.conf import settings

import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.user_login, name='user_login'),
    url(r'^logout/', views.user_logout, name='user_logout'),
    url(r'^register/', views.user_register, name='user_register'),
    url(r'^set_password/', views.set_password, name='set_password'),
    url(r'^static/(?P<path>.*)$', static_views.serve, name='static'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
