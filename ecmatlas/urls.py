# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

#from ecmatlas import views

urlpatterns = patterns('views',
    (r'^', include('cloud9expirement.urls')),
    
) 
