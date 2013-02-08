from django.conf.urls.defaults import *
from auxdb.personnel.views import aps1_pdf
from auxdb.personnel.views import aps11_html
from auxdb.personnel.views import aps10_html
from auxdb.personnel.models import Person

from django.views.generic import ListView
from django.views.generic import DetailView

urlpatterns = patterns('', 
                       url(r'^$', ListView.as_view(model=Person)), 
                       url(r'^person/(?P<pk>-?\d+)$', 
                           DetailView.as_view(model=Person)), 
                       url(r'^person/(?P<pk>-?\d+)/aps1.pdf$', aps1_pdf), 
                       url(r'^person/(?P<pk>-?\d+)/(?P<fy>\d{4})/aps11.html$', 
                           aps11_html), 
                       url(r'^ten/(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2}).html$', 
                           aps10_html, name='aps10_html'), 
                       )
                       
