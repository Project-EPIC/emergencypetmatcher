from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from home.models import * 

urlpatterns = patterns('reporting.views',

	url (r'^submit_PetReport', 'submit_PetReport', name='submit_PetReport'),
	url (r'^PetReport/(?P<petreport_id>\d+)/$','disp_PetReport',name='disp_PetReport'),
	# url (r'^get_PetReport_json/(?P<petreport_id>\d+)/$', 'get_PetReport_json', name="get_PetReport_json"),
	url (r'^bookmark_PetReport','bookmark_PetReport',name='bookmark_PetReport'),
	url (r'^bookmarks$','disp_bookmarks',name='bookmarks'),
)




