from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

urlpatterns = patterns('socializing.views',

	url (r'^(?P<userprofile_id>\d+)/$', 	"get", 						name='get_UserProfile'),
    url (r'^get_UserProfiles_JSON$',        'get_UserProfiles_JSON',  	name='get_UserProfiles_JSON'),
	url (r'^message$', 						"message", 					name="message_UserProfile"),
	url (r'^follow$',						"follow",					name='follow_UserProfile'),
	url (r'^unfollow$',						'unfollow',					name='unfollow_UserProfile'),
	url (r'^edit/update_info$', 			"update_info", 				name="update_info_UserProfile"),
	url (r'^edit/update_password$', 		"update_password", 			name="update_password_UserProfile"),
	url (r'^edit/(?P<userprofile_id>\d+)/', "edit", 					name='edit_UserProfile'),
	url (r'^delete', 						"delete", 					name='delete_UserProfile'),
	#email verification URL
	url(r'^email_verification_complete/(?P<activation_key>\w+)/$', "email_verification_complete", name='email_verification_complete_UserProfile'),
)
