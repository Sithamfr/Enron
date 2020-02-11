#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.menu, name='menu'),
    
    re_path(r'^search/$', views.recherche, name='recherche'),
    
    re_path(r'^employes/$', views.employ, name='employ'),
    
    re_path(r'^ref/$', views.ref, name='ref'),
    
    re_path(r'^mails_discu/$', views.discu, name='discu'),
    
]
