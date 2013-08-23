from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from home.models import * 

urlpatterns = patterns('reporting.views',

	url (r'^submit_PetReport', 'submit_PetReport', name='submit_PetReport'),
	url (r'^get_pet_breeds/(?P<pet_type>\d+)/$', 'get_pet_breeds', name="get_pet_breeds"),
	url (r'^PetReport/(?P<petreport_id>\d+)/$','get_PetReport',name='get_PetReport'),
	url (r'^bookmark_PetReport','bookmark_PetReport',name='bookmark_PetReport'),
)




