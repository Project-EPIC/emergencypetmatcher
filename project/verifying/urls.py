from django.conf.urls import include, url
from . import views

urlpatterns = [
  url (r'^(?P<petreunion_id>\d+)/$',                    views.get_PetReunion,       name='get_PetReunion'),
  url (r'^get_PetReunion_JSON$',                        views.get_PetReunion_JSON,  name='get_PetReunion_JSON'),
  url (r'^get_PetReunions_JSON$',                       views.get_PetReunions_JSON, name='get_PetReunions_JSON'),
  url (r'^check_PetMatch/(?P<petmatchcheck_id>\d+)/$',  views.verify,               name="verify_PetMatchCheck"),
]