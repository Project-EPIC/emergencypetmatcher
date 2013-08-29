from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from home.models import * 
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

urlpatterns = patterns('home.views',

	url (r'^$', 'home', name='home'),
	url (r'^get_activities_json$', 'get_activities_json', name="get_activities_json"),
	url (r'^get_PetReport/(?P<petreport_id>\d+)/$', 'get_PetReport', name="get_PetReport"),	
	url (r'^get_PetReports/(?P<page>\d+)/$', 'get_PetReports', name="get_PetReports"),
	url (r'^get_PetMatches/(?P<page>\d+)/$', 'get_PetMatches', name="get_PetMatches"),	
	url (r'^get_successful_PetMatches/(?P<page>\d+)/$','get_successful_PetMatches',name='get_successful_PetMatches'),
	url (r'^get_bookmarks/(?P<page>\d+)/$','get_bookmarks',name='get_bookmarks'),
	url (r'^login$', 'login_User', name='login_User'),
	url (r'^logout$', 'logout_User', name='logout_User'),
	url (r'^UserProfile/(?P<userprofile_id>\d+)/$', 'get_UserProfile_page', name='get_UserProfile_page'),
	url (r'^UserProfile/message_UserProfile$', "message_UserProfile", name="message_UserProfile"),
	url (r'^UserProfile/follow$','follow_UserProfile',name='follow_UserProfile'),
	url (r'^UserProfile/unfollow$','unfollow_UserProfile',name='unfollow_UserProfile'),	
	url (r'^UserProfile/edituserprofile/update_User_info$', "update_User_info", name="update_User_info"),
	url (r'^UserProfile/edituserprofile/update_User_password$', "update_User_password", name="update_User_password"),	
	url (r'^UserProfile/edituserprofile', 'editUserProfile_page', name='editUserProfile_page'),	
	url (r'^about$', 'about', name='about'),

	#Django-Social-Auth
	#url(r'^social_auth_login/([a-z]+)$', 'social_auth_login', name='users_social_auth_login'),
	url(r'^social_auth_get_details/$', 'social_auth_get_details', name='social_auth_get_details'),
	url(r'^', include('social_auth.urls')),

	#registration-related URLs that have been customized.
	url(r'^activate/complete/$', "registration_activation_complete", name='registration_activation_complete'),

	# Activation keys get matched by \w+ instead of the more specific
	# [a-fA-F0-9]{40} because a bad activation key should still get to the view;
	# that way it can return a sensible "invalid key" message instead of a
	# confusing 404.
	url(r'^activate/(?P<activation_key>\w+)/$', "registration_activate", {'backend':'registration.backends.default.DefaultBackend'}, name='registration_activate'),
	url(r'^register/complete/$', "registration_complete", name='registration_complete'),
	url(r'^register/closed/$', "registration_disallowed", name='registration_disallowed'),
 	url(r'^accounts/register/$', "registration_register",  name='registration_register' ),
 	url(r'^accounts/activate/complete/$', "registration_activation_complete"),
 	url(r'^accounts/password/reset/complete/$', 'password_reset_complete', name="password_reset_complete"),
 	url(r'^accounts/password/reset/done/$', 'password_reset_done', name="password_reset_done"),
	url (r'^accounts/', include('registration.backends.default.urls')),

	#email verification URL
	url(r'^email_verification_complete/(?P<activation_key>\w+)/$', "email_verification_complete", name='email_verification_complete'),
	
)

# urlpatterns += staticfiles_urlpatterns()
