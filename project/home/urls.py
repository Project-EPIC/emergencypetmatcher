from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from home.models import * 

urlpatterns = patterns('home.views',

	url (r'^$','home', name='home'),
	url (r'^login$', 'login_user', name='login_user'),
	url (r'^logout$', 'logout_user', name='logout'),
	url (r'^(?P<userprofile_id>\d+)/$', 'detail', name='detail'),
	url (r'^', include('social_auth.urls')),
	url (r'^social_auth_login/([a-z]+)$', 'social_auth_login', name='users_social_auth_login'),
	url (r'^form/$', 'form', name='form'),
	
)