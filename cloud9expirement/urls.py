from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

from cloud9expirement import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cloud9expirement.views.home', name='home'),
    # url(r'^cloud9expirement/', include('cloud9expirement.foo.urls')),
    
    # These are the file upload and parsers.  These are Dangerous for
    # the database.  There is no safety in place to undo anything. 
    url(r'^list/', views.list, name='list'),
    url(r'^expunge/', views.expunge, name='expunge'),
    url(r'^documents/', views.parseDocument, name='parseDocument'),
    url(r'^datainput.html', views.datainput, name='datainput'),
    url(r'validate/', views.validate, name='validate'),
    url(r'validate.ProteinHitsUpdate/', view=views.ProteinHitsUpdate.as_view(), name='ProteinHitsUpdate'),
    url(r'validate.ArticalUpdate/', view=views.ArticalUpdate.as_view(), name='ArticalUpdate'),
    url(r'validate.ProteinsUpdate/', view=views.ProteinHitsUpdate.as_view(), name='ProteinHitsUpdate'),
    url(r'validate.ExperimentsUpdate/', view=views.ExperimentsUpdate.as_view(), name='ExperimentsUpdate'),
    url(r'validate.VariableModificationsUpdate/', view=views.VariableModificationsUpdate.as_view(), name='VariableModificationsUpdate'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls), name='admin'),
    
    url(r'^protein/(?P<protein_id>\d+)/$', views.protein, name='protein'),
    url(r'^experiment/(?P<experiment_id>\d+)/$', views.experiment, name='experiment'),

    url(r'^introduction.html', views.introduction, name='introduction'),
    url(r'^introduction2.html', views.introduction2, name='introduction2'),
    url(r'^introduction3.html', views.introduction3, name='introduction3'),
    url(r'^ecmproteins.html', views.ecmproteins, name='ecmproteins'),
    url(r'^experiment_type.html', views.experiment_type, name='experiment_type'),
    url(r'^tissues.html', views.tissues, name='tissues'),

    url(r'^readout_and_output.html', views.readout_and_output, name='readout_and_output'),

    url(r'^csv_download', views.csv_download, name='csv_download'),
    url(r'^search.html', views.search, name='search'),
    url(r'^results2.html', views.results2, name='results2'),
    url(r'^results.html', views.results, name='results'),
    url(r'^stats.html', views.stats, name='stats'),
    url(r'^links.html', views.links, name='links'),
    url(r'^projects.html', views.projects, name='projects'),
    url(r'^advanceSearch.html', views.advanceSearch, name='advanceSearch'),
    url(r'^methods.html', views.methods, name='methods'),
    url(r'^contact.html', views.contact, name='contact'),
    url(r'^', views.index, name='index'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

