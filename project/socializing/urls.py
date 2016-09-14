from django.conf.urls import include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

	url (r'^(?P<userprofile_id>\d+)/$', 	views.get, 						name='get_UserProfile'),
    url (r'^get_UserProfiles_JSON$',        views.get_UserProfiles_JSON,  	name='get_UserProfiles_JSON'),
	url (r'^message$', 						views.message, 					name="message_UserProfile"),
	url (r'^follow$',						views.follow,					name='follow_UserProfile'),
	url (r'^unfollow$',						views.unfollow,					name='unfollow_UserProfile'),
	url (r'^edit/update_info$', 			views.update_info, 				name="update_info_UserProfile"),
	url (r'^edit/update_password$', 		views.update_password, 			name="update_password_UserProfile"),
	url (r'^edit/(?P<userprofile_id>\d+)/', views.edit, 					name='edit_UserProfile'),
	url (r'^delete', 						views.delete, 					name='delete_UserProfile'),
	#email verification URL
	url(r'^email_verification_complete/(?P<activation_key>\w+)/$', views.email_verification_complete, name='email_verification_complete_UserProfile'),
]
