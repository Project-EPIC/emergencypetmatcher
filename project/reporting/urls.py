from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from socializing.models import UserProfile

urlpatterns = patterns('reporting.views',
    url (r'^(?P<petreport_id>\d+)/$',                           'get',                  name='get_PetReport'),
    url (r'^get_PetReport_JSON$',                               'get_PetReport_JSON',   name='get_PetReport_JSON'),
    url (r'^get_PetReports_JSON$',                              'get_PetReports_JSON',  name='get_PetReports_JSON'),
    url (r'^edit/(?P<petreport_id>\d+)/$',                      'edit',                 name='edit_PetReport'),
    url (r'^close/(?P<petreport_id>\d+)/$',                     'close',                name='close_PetReport'),
    url (r'^new',                                               'submit',               name='submit_PetReport'),
    url (r'^bookmark',                                          'bookmark',             name='bookmark_PetReport'),
    url (r'^get_pet_breeds$',                                   'get_pet_breeds',       name="get_pet_breeds"),
    url (r'^get_event_tags$',                                   'get_event_tags',       name='get_event_tags'),
    url (r'^mixed0$',                                           'mixed0',               name='mixed0'),
    url (r'^mixed1/(?P<petmatch_id>\d+)/$',                     'mixed1',               name='mixed1'),
    url (r'^mixed2/(?P<petreport_id>\d+)/$',                    'mixed2',               name='mixed2'),
    url (r'^mixed3/(?P<target_id>\d+)/(?P<candidate_id>\d+)/$', 'mixed3',               name='mixed3'),
    url (r'^mixed4/(?P<petmatch_id>\d+)/$',                     'mixed4',               name='mixed4'),
)
