from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from home.models import * 

urlpatterns = patterns('matching.views',

	# url (r'^$', 'matching', name='matching'),
	url (r'^match_petreport/(?P<petreport_id>\d+)/$','match_petreport',name='match_petreport'),
	url (r'^propose_match/(?P<target_petreport_id>\d+)/(?P<candidate_petreport_id>\d+)/$', 'propose_match', name='propose_match'),

)


