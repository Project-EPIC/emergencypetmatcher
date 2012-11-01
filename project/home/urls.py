from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from home.models import * 
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

urlpatterns = patterns('home.views',

	url(r'^$', 'home', name='home'),
	url(r'^get_activities_json$', 'get_activities_json', name="get_activities_json"),	
	url(r'^login$', 'login_User', name='login_User'),
	url(r'^logout$', 'logout_User', name='logout_User'),
	url(r'^UserProfile/(?P<userprofile_id>\d+)/$', 'get_UserProfile_page', name='get_UserProfile_page'),
	url(r'^social_auth_login/([a-z]+)$', 'social_auth_login', name='users_social_auth_login'),
	url(r'^get_social_details/$', 'get_social_details', name='get_social_details'),
	url (r'^follow/(?P<userprofile_id1>\d+)/(?P<userprofile_id2>\d+)/$','follow',name='follow'),
	url (r'^unfollow/(?P<userprofile_id1>\d+)/(?P<userprofile_id2>\d+)/$','unfollow',name='unfollow'),
	url(r'^', include('social_auth.urls')),
	url(r'^edituserprofile/$', 'editUserProfile_page', name='editUserProfile_page'),
	url (r'^accounts/', include('registration.backends.default.urls')),
	#registration-related URLs that have been customized.
	url(r'^activate/complete/$', "registration_activation_complete", name='registration_activation_complete'),
	url(r'^register/complete/$', "registration_complete", name='registration_complete'),
	url(r'^register/closed/$', "registration_disallowed", name='registration_disallowed'),
	#email verification URL
	url(r'^email_verification_complete/(?P<activation_key>\w+)/$', "email_verification_complete", name='email_verification_complete'),
	
	
)

# urlpatterns += staticfiles_urlpatterns()
