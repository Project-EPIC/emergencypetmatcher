from django.conf.urls import include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from socializing.models import UserProfile
from . import views

urlpatterns = [
    url (r'^(?P<petreport_id>\d+)/$',        	views.get,                  name='get_PetReport'),
    url (r'^get_PetReport_JSON$',            	views.get_PetReport_JSON,   name='get_PetReport_JSON'),
    url (r'^get_PetReports_JSON$',           	views.get_PetReports_JSON,  name='get_PetReports_JSON'),
    url (r'^edit/(?P<petreport_id>\d+)/$',   	views.edit,                 name='edit_PetReport'),
    url (r'^close/(?P<petreport_id>\d+)/$',	 	views.close,                name='close_PetReport'),
    url (r'^new',								views.submit,               name='submit_PetReport'),
    url (r'^bookmark',							views.bookmark,             name='bookmark_PetReport'),
    url (r'^get_pet_breeds$',					views.get_pet_breeds,       name="get_pet_breeds"),
    url (r'^get_event_tags$',					views.get_event_tags,       name='get_event_tags'),
]
