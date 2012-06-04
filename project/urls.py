from django.conf.urls.defaults import patterns, include, url
import auth

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^reporting/', include('reporting.urls')),
    url(r'^auth/', include('auth.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^$', 'auth.views.home', name="home"),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
