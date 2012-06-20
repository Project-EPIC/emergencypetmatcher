from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from home.models import * 



urlpatterns = patterns('home.views',

	url (r'^$','index', name='index'),
)