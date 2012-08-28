from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from home.models import * 

urlpatterns = patterns('home.views',

	url (r'^$','home', name='home'),
	url (r'^login$', 'login_User', name='login_User'),
	url (r'^logout$', 'logout_User', name='logout_User'),
	url (r'^UserProfile/(?P<userprofile_id>\d+)/$', 'get_UserProfile_page', name='get_UserProfile_page'),
	url (r'^social_auth_login/([a-z]+)$', 'social_auth_login', name='users_social_auth_login'),
	url (r'^form/$', 'form', name='form'),
	url(r'^share_(?P<petreport_id>\d+)/$', 'share', name='share'),
	url (r'^', include('social_auth.urls')),
	
)