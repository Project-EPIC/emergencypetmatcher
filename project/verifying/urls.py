from django.conf.urls import patterns, include, url

urlpatterns = patterns('verifying.views',
	url (r'^verify_PetMatch/(?P<petmatch_id>\d+)/$', "verify_PetMatch", name="verify_PetMatch"),
)


