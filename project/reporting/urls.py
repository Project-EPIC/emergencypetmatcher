from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from home.models import * 

urlpatterns = patterns('reporting.views',

	url (r'^submit_petreport', 'submit_petreport', name='submit_petreport'),
	url (r'^petreport/(?P<petreport_id>\d+)/$','disp_petreport',name='disp_petreport'),
	url (r'^get_petreport_json/(?P<petreport_id>\d+)/$', 'get_petreport_json', name="get_petreport_json"),
	url(r'^bookmark$','bookmark_petreport',name='bookmark_petreport'),
	# url (r'^petreport/(?P<user_id>\d+)/(?P<petreport_id>\d+)/$','bookmark_petreport',name='bookmark_petreport'),

)




