from django.conf.urls import include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from socializing.models import UserProfile
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	url (r'^$', 						views.home, 			name= "home"),
	url (r'^get_activities$', 			views.get_activities, 	name="get_activities"),
	url (r'^get_bookmarks$',			views.get_bookmarks,	name="get_bookmarks"),
	url (r'^login$', 					views.login_User,		name="login_User"),
	url (r'^logout$', 					views.logout_User,		name="logout_User"),
	url (r'^about$', 					views.about,			name="about"),
	url (r'^stats$', 					views.stats,			name="stats"),

	#Python-Social-Auth
	url(r'^', include('social.apps.django_app.urls', namespace='social')),

	#registration-related URLs that have been customized.
	url(r'^activate/complete/$', views.registration_activation_complete, name="registration_activation_complete"),

	url(r'^accounts/register/$', views.registration_register, name="registration_register"),
	url(r'^register/complete/$', views.registration_complete, name="registration_complete"),
	url(r'^register/closed/$', views.registration_disallowed, name="registration_disallowed"),
 	url(r'^accounts/activate/complete/$', views.registration_activation_complete, name="registration_activation_complete"),
	url(r'^accounts/activate/(?P<activation_key>\w+)/$', views.registration_activate, {'backend':'registration.backends.default.DefaultBackend'}, name="registration_activate"),
	url(r'^accounts/activate/guardian/(?P<guardian_activation_key>\w+)/$', views.registration_guardian_activate, name="registration_guardian_activate"),
 	url(r'^accounts/password/reset/complete/$', views.password_reset_complete, name="password_reset_complete"),
 	url(r'^accounts/password/reset/done/$', views.password_reset_done, name="password_reset_done"),
 	url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, name="password_reset_confirm"),
	url(r'^accounts/', include('registration.backends.default.urls')),
]
