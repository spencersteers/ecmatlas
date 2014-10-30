#from django.conf.urls import patterns, url
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.urlpatterns import format_suffix_patterns
from ecmdatabase import views

urlpatterns = patterns('',
    url(r'^proteins/$', views.ProteinList.as_view()),
    url(r'^proteins/(?P<pk>[0-9]+)/$', views.ProteinDetail.as_view()),
    
    url(r'^tissues/$', views.TissueList.as_view()),
    url(r'^tissues/(?P<pk>[0-9]+)/$', views.TissueDetail.as_view()),

    url(r'^experiments/$', views.ExperimentList.as_view()),
    url(r'^experiments/(?P<pk>[0-9]+)/$', views.ExperimentDetail.as_view()),

    url(r'^proteinhits/$', views.ProteinHitList.as_view()),
    url(r'^proteinhits/(?P<pk>[0-9]+)/$', views.ProteinHitDetail.as_view()),

    url(r'^variablemodifications/$', views.VariableModificationList.as_view()),
    url(r'^variablemodifications/(?P<pk>[0-9]+)/$', views.VariableModificationDetail.as_view()),
) 
