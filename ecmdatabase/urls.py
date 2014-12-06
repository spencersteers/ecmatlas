#from django.conf.urls import patterns, url
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.urlpatterns import format_suffix_patterns
from ecmdatabase import views

urlpatterns = patterns('',
    url(r'^proteins/$', views.ProteinList.as_view(), name='protein-list'),
    url(r'^proteins/(?P<pk>[0-9]+)/$', views.ProteinDetail.as_view(), name='protein-detail'),

    url(r'^tissues/$', views.TissueList.as_view()),
    url(r'^tissues/(?P<pk>[0-9]+)/$', views.TissueDetail.as_view()),

    url(r'^datasets/insert/(?P<dataset_id>[0-9]+)$', views.dataset_insert, name="datasets-insert"),
    url(r'^datasets/upload/$', views.dataset_upload),
)
