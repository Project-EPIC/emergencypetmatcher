from django.conf.urls import patterns, include, url
from django.contrib import admin
import urllib2

admin.autodiscover()

urlpatterns = patterns('',

	url(r'^$', include('social_auth.urls')),
	url (r'^$', include ('home.urls')),
	url(r'^reporting/', include ('reporting.urls')),
	# Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'epic_site', urllib2.urlopen('http://epic.cs.colorado.edu'))

	
    
    

    
)
