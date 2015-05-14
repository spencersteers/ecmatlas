#from django.conf.urls import patterns, url
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.urlpatterns import format_suffix_patterns
from experiments import views


urlpatterns = patterns('',
    url(r'^experiments/$', views.ExperimentList.as_view()),
    url(r'^experiments/(?P<pk>[0-9]+)/$', views.ExperimentDetail.as_view()),
    url(r'^datasets/$', views.DatasetList.as_view()),
    url(r'^datasets/(?P<pk>[0-9]+)/$', views.DatasetDetail.as_view()),
    url(r'^datasetitems/$', views.DatasetItemList.as_view()),
    url(r'^datasetitems/(?P<pk>[0-9]+)/$', views.DatasetItemDetail.as_view()),
    url(r'^relativeconcentrations/$', views.RelativeConcentrationList.as_view()),
    url(r'^relativeconcentrations/(?P<pk>[0-9]+)/$', views.RelativeConcentrationDetail.as_view()),
)
