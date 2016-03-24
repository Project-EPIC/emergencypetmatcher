from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from socializing.models import UserProfile

urlpatterns = patterns('reporting.views',
    url (r'^(?P<petreport_id>\d+)/$',       'get',                  name='get_PetReport'),
    url (r'^get_PetReport_JSON$',           'get_PetReport_JSON',   name='get_PetReport_JSON'),
    url (r'^get_PetReports_JSON$',          'get_PetReports_JSON',  name='get_PetReports_JSON'),
    url (r'^edit/(?P<petreport_id>\d+)/$',  'edit',                 name='edit_PetReport'),
    url (r'^close/(?P<petreport_id>\d+)/$', 'close',                name='close_PetReport'),
    url (r'^new',                           'new',                  name='new_PetReport'),
    url (r'^submit',                        'submit',               name='submit_PetReport'),
    url (r'^bookmark',                      'bookmark',             name='bookmark_PetReport'),
    url (r'^get_pet_breeds$',               'get_pet_breeds',       name="get_pet_breeds"),
    url (r'^get_event_tags$',               'get_event_tags',       name='get_event_tags'),
    url (r'^mixed',                         'mixed',                name='mixed'),
    url (r'^choice',                        'choice',               name='choice'),
)
