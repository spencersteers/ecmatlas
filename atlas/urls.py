#from django.conf.urls import patterns, url
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from rest_framework.urlpatterns import format_suffix_patterns
from atlas import views

urlpatterns = patterns('',
    url(r'^tissueweightnorm/average$', views.tissueweightnorm_average),
)
