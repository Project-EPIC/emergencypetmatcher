from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

	url (r'^', include ('home.urls')),
	url (r'^users/', include ('socializing.urls')),
	url (r'^reporting/', include('reporting.urls')),
	url (r'^matching/', include ('matching.urls')),
	url (r'^verifying/', include ('verifying.urls')),
	# Uncomment the next line to enable the admin:
  url (r'^admin/', include(admin.site.urls)),

)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)