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
                  url(r'^book/detail$', views.book_detail, name='book_detail'),
                  url(r'^search/', views.book_search, name='book_search'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
