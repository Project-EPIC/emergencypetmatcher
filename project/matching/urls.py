from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView

urlpatterns = patterns('matching.views',
  url (r'^(?P<petmatch_id>\d+)/$','get_PetMatch', name='get_PetMatch'),
	url (r'^new/(?P<petreport_id>\d+)/$','match', name='match'),
  url (r'^get_candidate_PetReports/$','get_candidate_PetReports', name='get_candidate_PetReports'),
	url (r'^propose/(?P<target_petreport_id>\d+)/(?P<candidate_petreport_id>\d+)/$', 'propose', name='propose'),
	url (r'^vote', "vote", name="vote")
)


