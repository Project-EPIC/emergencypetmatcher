from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from home.models import * 



urlpatterns = patterns('home.views',

	url (r'^$','home', name='home'),
	url (r'^$', 'social_login', name='social_login'),
	url (r'^', include('social_auth.urls')),
	url(r'^form/$', 'form', name='form'),
	
)