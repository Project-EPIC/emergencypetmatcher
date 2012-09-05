from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from django.views.generic.simple import direct_to_template
from home.models import * 

urlpatterns = patterns('matching.views',
	
	url (r'^match_PetReport/(?P<petreport_id>\d+)/$','match_PetReport', name='match_PetReport'),
	url (r'^propose_PetMatch/(?P<target_petreport_id>\d+)/(?P<candidate_petreport_id>\d+)/$', 'propose_PetMatch', name='propose_PetMatch'),
	url (r'^PetMatch/(?P<petmatch_id>\d+)/$','display_PetMatch', name='display_PetMatch'),
	url (r'^vote_PetMatch', "vote_PetMatch", name="vote_PetMatch"),
)


