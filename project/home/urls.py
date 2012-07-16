from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from home.models import * 



urlpatterns = patterns('home.views',

	url (r'^$','home', name='home'),
	url (r'^users/(?P<userprofile_id>\d+)/$', 'detail', name='detail'),
	url (r'^', include('social_auth.urls')),
	url (r'^social_auth_login/([a-z]+)$', 'social_auth_login', name='users_social_auth_login'),
	url (r'^form/$', 'form', name='form'),
	url(r'^share_(?P<petreport_id>\d+)/$', 'share', name='share'),
	
)