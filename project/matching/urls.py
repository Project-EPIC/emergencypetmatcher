from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from home.models import * 

urlpatterns = patterns('matching.views',

	url (r'^$', 'matching', name='matching'),
)


