from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
# from tastypie.api import Api

# user_resource = UserResource()
# userprofile_resource = UserProfileResource()
# petreport_resource = PetReportResource()
# v1_api = Api(api_name='v1')
# v1_api.register(UserResource())
# v1_api.register(UserProfileResource())
# v1_api.register(PetReportResource())
# v1_api.register(PetReportResource2())

admin.autodiscover()

urlpatterns = patterns('',

	url (r'^', include ('home.urls')),
	url (r'^users/', include ('social.urls')),
	url (r'^reporting/', include('reporting.urls')),
	url (r'^matching/', include ('matching.urls')),
	url (r'^verifying/', include ('verifying.urls')),
	# Uncomment the next line to enable the admin:
    url (r'^admin/', include(admin.site.urls)),
	# url (r'^api/', include(user_resource.urls)),
	# url (r'^api/', include(userprofile_resource.urls)),
 #    url (r'^api/', include(petreport_resource.urls)),    
 #    url (r'^api/', include(v1_api.urls)),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#This is for development - MAKE SURE TO TURN OFF for Production!
