from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from home.models import * 



urlpatterns = patterns('home.views',

	url (r'^$','home', name='home'),
	url (r'^login_page/', include('social_auth.urls')),
	url (r'^login_page$', 'login_page', name='login_page'),
	url (r'^register_page$', 'register_page', name='register_page'),
	url (r'^login$','login_user', name='login_user'),
	url (r'^logout$','logout_user', name='logout_user'),
	url (r'^register$','register_user', name='register_user'),
	url (r'^social_login$', 'social_login', name='social_login'),
	url(r'^form/$', 'form', name='form'),
	
)