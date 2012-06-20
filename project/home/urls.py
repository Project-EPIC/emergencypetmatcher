from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from home.models import * 



urlpatterns = patterns('home.views',

	url (r'^$','home', name='home'),
	url (r'^login_page$', 'login_page', name='login_page'),
	url (r'^signup_page$', 'signup_page', name='signup_page'),
	url (r'^login/','login_user', name='login_user'),
	url (r'^logout/','logout_user', name='logout_user'),
	url (r'^signup/','signup_user', name='signup_user'),
	
)