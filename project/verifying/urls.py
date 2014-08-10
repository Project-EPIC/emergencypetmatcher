from django.conf.urls import patterns, include, url

urlpatterns = patterns('verifying.views',
	url (r'^(?P<petcheck_id>\d+)/$', "verify_PetCheck", name="verify_PetCheck"),
)


