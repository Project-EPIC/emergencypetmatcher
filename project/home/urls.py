from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from socializing.models import UserProfile 
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

urlpatterns = patterns('home.views',
	url (r'^$', 'home', name='home'),
	url (r'^get_activities/$', 'get_activities', name="get_activities"),	
	url (r'^get_bookmarks/$','get_bookmarks',name='get_bookmarks'),
	url (r'^login$', 'login_User', name='login_User'),
	url (r'^logout$', 'logout_User', name='logout_User'),
	url (r'^about$', 'about', name='about'),

	#Python-Social-Auth
	url(r'^', include('social.apps.django_app.urls', namespace='social')),

	#registration-related URLs that have been customized.
	url(r'^activate/complete/$', "registration_activation_complete", name='registration_activation_complete'),

	# Activation keys get matched by \w+ instead of the more specific
	# [a-fA-F0-9]{40} because a bad activation key should still get to the view;
	# that way it can return a sensible "invalid key" message instead of a
	# confusing 404.
	url(r'^accounts/register/$', "registration_register",  name='registration_register' ),
	url(r'^register/complete/$', "registration_complete", name='registration_complete'),
	url(r'^register/closed/$', "registration_disallowed", name='registration_disallowed'),	
 	url(r'^accounts/activate/complete/$', "registration_activation_complete"),	
	url(r'^accounts/activate/(?P<activation_key>\w+)/$', "registration_activate", {'backend':'registration.backends.default.DefaultBackend'}, name='registration_activate'),
	url(r'^accounts/activate/guardian/(?P<guardian_activation_key>\w+)/$', "registration_guardian_activate", name="registration_guardian_activate"),
 	url(r'^accounts/password/reset/complete/$', 'password_reset_complete', name="password_reset_complete"),
 	url(r'^accounts/password/reset/done/$', 'password_reset_done', name="password_reset_done"),
 	url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name='auth_password_reset_confirm'), 	
	url(r'^accounts/', include('registration.backends.default.urls')),
)
