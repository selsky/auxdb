from django.conf.urls.defaults import *
from auxdb.personnel.views import aps1_pdf
from auxdb.personnel.models import Person

from django.views.generic import ListView
from django.views.generic import DetailView

urlpatterns = patterns('', 
                       url(r'^$', ListView.as_view(model=Person)), 
                       url(r'^person/(?P<pk>-?\d+)$', DetailView.as_view(model=Person)), 
                       url(r'^person/(?P<pk>-?\d+)/aps1.pdf$', aps1_pdf), 
                       )
                       
