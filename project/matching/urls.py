from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView

urlpatterns = patterns('matching.views',
    url (r'^get_PetMatch_JSON$',                                    'get_PetMatch_JSON',                name='get_PetMatch_JSON'),
    url (r'^get_PetMatches_JSON$',                                  'get_PetMatches_JSON',              name='get_PetMatches_JSON'),
    url (r'^(?P<petmatch_id>\d+)/$',                                'get_PetMatch',                     name='get_PetMatch'),
    url (r'^new/(?P<petreport_id>\d+)$',                            'match',                            name='match_PetMatch'),
    url (r'^get_candidate_PetReports_JSON$',                        'get_candidate_PetReports',         name='get_candidate_PetReports_JSON'),
    url (r'^vote/(?P<petmatch_id>\d+)',                             "vote",                             name="vote_PetMatch"),
    url (r'^propose/(?P<target_id>\d+)/(?P<candidate_id>\d+)/$',    'propose',                          name='propose_PetMatch'),

)
