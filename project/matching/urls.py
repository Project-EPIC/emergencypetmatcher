from django.conf.urls import include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url (r'^get_PetMatch_JSON$',                               		views.get_PetMatch_JSON,                name='get_PetMatch_JSON'),
    url (r'^get_PetMatches_JSON$',                                  views.get_PetMatches_JSON,              name='get_PetMatches_JSON'),
    url (r'^(?P<petmatch_id>\d+)/$',                                views.get,                              name='get_PetMatch'),
    url (r'^new/(?P<petreport_id>\d+)$',                            views.match,                            name='match_PetMatch'),
    url (r'^get_candidate_PetReports_JSON$',                        views.get_candidate_PetReports,         name='get_candidate_PetReports_JSON'),
    url (r'^vote/(?P<petmatch_id>\d+)',                             views.vote,                             name="vote_PetMatch"),
    url (r'^propose/(?P<target_id>\d+)/(?P<candidate_id>\d+)/$',    views.propose,                          name='propose_PetMatch'),
]
