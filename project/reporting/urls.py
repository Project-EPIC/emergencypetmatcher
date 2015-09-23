from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from socializing.models import UserProfile 

urlpatterns = patterns('reporting.views',
  url (r'^get_PetReport_JSON/$', 'get_PetReport_JSON', name='get_PetReport_JSON'),
  url (r'^get_PetReports_JSON/$', 'get_PetReports_JSON', name='get_PetReports_JSON'),
  url (r'^(?P<petreport_id>\d+)/$', 'get_PetReport', name='get_PetReport'),
  url (r'^edit/(?P<petreport_id>\d+)/$', 'edit', name='edit'),
	url (r'^new', 'submit', name='submit'),
	url (r'^bookmark','bookmark', name='bookmark'),
  url (r'^get_pet_breeds/(?P<pet_type>\d+)/$', 'get_pet_breeds', name="get_pet_breeds"),
)




