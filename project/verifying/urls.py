from django.conf.urls import patterns, include, url

urlpatterns = patterns('verifying.views',
  url (r'^(?P<petreunion_id>\d+)/$',                    'get_PetReunion',       name='get_PetReunion'),
  url (r'^get_PetReunion_JSON$',                        'get_PetReunion_JSON',  name='get_PetReunion_JSON'),
  url (r'^get_PetReunions_JSON$',                       'get_PetReunions_JSON', name='get_PetReunions_JSON'),
  url (r'^check_PetMatch/(?P<petmatchcheck_id>\d+)/$',  "verify",               name="verify_PetMatchCheck"),
)
