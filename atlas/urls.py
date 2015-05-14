#from django.conf.urls import patterns, url
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.urlpatterns import format_suffix_patterns

from atlas import views


urlpatterns = patterns('',
    url(r'^proteins/$', views.Proteins.as_view(), name='protein-list'),
    url(r'^proteins/(?P<pk>[0-9]+)/$', views.ProteinDetail.as_view(), name='protein-detail'),

    url(r'^tissues/$', views.TissueList.as_view()),
    # url(r'^tissues/all/$', views.TissueList.as_view()),
    url(r'^tissues/(?P<pk>[0-9]+)/$', views.TissueDetail.as_view()),
    # url(r'^tissues/(?P<slug>[\w-]+)/$', views.TissueDetail.as_view()),

    url(r'^families/$', views.FamilyList.as_view()),
    url(r'^families/(?P<pk>[0-9]+)/$', views.FamilyDetail.as_view()),

    url(r'^functionalgroups/$', views.FunctionalGroupList.as_view()),
    url(r'^functionalgroups/(?P<pk>[0-9]+)/$', views.FunctionalGroupDetail.as_view()),
)
