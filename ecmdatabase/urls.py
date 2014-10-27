from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from ecmdatabase import views

urlpatterns = patterns('',
    url(r'^proteins/$', views.ProteinList.as_view()),
    url(r'^proteins/(?P<pk>[0-9]+)/$', views.ProteinDetail.as_view()),
    
    url(r'^tissues/$', views.TissueList.as_view()),
    url(r'^tissues/(?P<pk>[0-9]+)/$', views.TissueDetail.as_view()),
)
