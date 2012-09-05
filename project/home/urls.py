from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from home.models import * 
from django.contrib.auth import views as auth_views

urlpatterns = patterns('home.views',

	url(r'^$', 'home', name='home'),	
	url(r'^login$', 'login_User', name='login_User'),
	url(r'^logout$', 'logout_User', name='logout_User'),
	url(r'^UserProfile/(?P<userprofile_id>\d+)/$', 'get_UserProfile_page', name='get_UserProfile_page'),
	url(r'^social_auth_login/([a-z]+)$', 'social_auth_login', name='users_social_auth_login'),
	url(r'^form/$', 'form', name='form'),
	url(r'^share_(?P<petreport_id>\d+)/$', 'share', name='share'),
	url(r'^', include('social_auth.urls')),

	url (r'^accounts/', include('registration.backends.default.urls')),
	#registration-related URLs that have been customized.
	url(r'^activate/complete/$', "registration_activation_complete", name='registration_activation_complete'),
	url(r'^register/complete/$', "registration_complete", name='registration_complete'),
	url(r'^register/closed/$', "registration_disallowed", name='registration_disallowed'),
	
)