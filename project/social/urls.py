from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from social.models import UserProfile 
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

urlpatterns = patterns('social.views',

	url (r'^(?P<userprofile_id>\d+)/$', 'get_UserProfile_page', name='get_UserProfile_page'),
	url (r'^message_UserProfile$', "message_UserProfile", name="message_UserProfile"),
	url (r'^follow$','follow_UserProfile',name='follow_UserProfile'),
	url (r'^unfollow$','unfollow_UserProfile',name='unfollow_UserProfile'),	
	url (r'^edit_userprofile/update_User_info$', "update_User_info", name="update_User_info"),
	url (r'^edit_userprofile/update_User_password$', "update_User_password", name="update_User_password"),	
	url (r'^edit_userprofile', 'editUserProfile_page', name='editUserProfile_page'),		
	#email verification URL
	url(r'^email_verification_complete/(?P<activation_key>\w+)/$', "email_verification_complete", name='email_verification_complete'),	
)



# urlpatterns += staticfiles_urlpatterns()
