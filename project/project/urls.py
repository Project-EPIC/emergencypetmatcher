from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from home.api import UserResource, UserProfileResource, PetReportResource

user_resource = UserResource()
userprofile_resource = UserProfileResource()
petreport_resource = PetReportResource()

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(UserProfileResource())
v1_api.register(PetReportResource())


admin.autodiscover()

urlpatterns = patterns('',

	url (r'^', include ('home.urls')),
	url (r'^reporting/', include('reporting.urls')),
	url (r'^matching/', include ('matching.urls')),
	# Uncomment the next line to enable the admin:
    url (r'^admin/', include(admin.site.urls)),

	url (r'^api/', include(user_resource.urls)),
	url (r'^api/', include(userprofile_resource.urls)),
    url (r'^api/', include(petreport_resource.urls)),    
    url (r'^api/', include(v1_api.urls)),

)
