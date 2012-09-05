from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',

	url (r'^', include ('home.urls')),
	url (r'^reporting/', include('reporting.urls')),
	url (r'^matching/', include ('matching.urls')),
	# Uncomment the next line to enable the admin:
    url (r'^admin/', include(admin.site.urls)),
    
)
