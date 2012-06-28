from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from django.views.generic import RedirectView
from home.models import * 

urlpatterns = patterns('reporting.views',

	url (r'^submit_petreport', 'submit_petreport', name='submit_petreport'),
)




