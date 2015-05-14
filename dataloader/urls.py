#from django.conf.urls import patterns, url
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.urlpatterns import format_suffix_patterns
from dataloader import views


urlpatterns = patterns('',
    url(r'^dataloader/datasets/insert/(?P<dataset_id>[0-9]+)/$', views.dataset_insert, name="datasets-insert"),
    url(r'^dataloader/datasets/delete/(?P<dataset_id>[0-9]+)/$', views.dataset_delete, name="datasets-delete"),
    url(r'^dataloader/datasets/upload/$', views.dataset_upload, name="datasets-upload"),
    url(r'^dataloader/datasets/files/$', views.dataset_uploadfiles, name="datasets-uploadfiles"),
)
