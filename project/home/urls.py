from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from home.models import * 
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('home.views',

	url (r'^$','home', name='home'),
	url (r'^login$', 'login_User', name='login_User'),
	url (r'^logout$', 'logout_User', name='logout_User'),
	url (r'^UserProfile/(?P<userprofile_id>\d+)/$', 'get_UserProfile_page', name='get_UserProfile_page'),
	url (r'^social_auth_login/([a-z]+)$', 'social_auth_login', name='users_social_auth_login'),
	url (r'^form/$', 'form', name='form'),
	url (r'^follow/(?P<userprofile_id1>\d+)/(?P<userprofile_id2>\d+)/$','follow',name='follow'),
	url (r'^unfollow/(?P<userprofile_id1>\d+)/(?P<userprofile_id2>\d+)/$','unfollow',name='unfollow'),

	url (r'^', include('social_auth.urls')),
	
)

urlpatterns += staticfiles_urlpatterns()