"""
WSGI config for project project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""

import os, sys, django
import site
from django.core.wsgi import get_wsgi_application

os.environ ["DJANGO_SETTINGS_MODULE"] = "project.settings"

#Path Constants (relative to project directory) - edit this to reflect changes in project WSGI script.
PROJECT_NAME = '/project'
SITE_PACKAGES = '/lib/python2.7/site-packages'

#This is the project_settings folder (django 1.4) that hosts the settings.py, urls.py, and ''this'' file.
project_settings_folder = os.path.dirname(__file__)

#This is the project directory path where the Django project and its apps should live.
project_folder = os.path.dirname(project_settings_folder)

#This is the EPM workspace directory path (root directory) of the entire EPM project. One of its children should be the project directory.
workspace = os.path.dirname(project_folder)

#Need to execute virtualenv.                                                                                                                                                                                                                                                                                                  
activate_this = os.path.join(project_folder, "bin/activate_this.py")
execfile(activate_this, dict(__file__=activate_this))

#We append the EPM directory path to SYS PATH.
sys.path.append(project_folder)
sys.path.append(project_settings_folder)

#We need to make sure we add in all of our local Python modules here.
site.addsitedir(workspace + SITE_PACKAGES)

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
application = django.core.handlers.wsgi.WSGIHandler()

#This is how you can test if its working. You should get a "Hello World!" to the browser screen.
#def application(environ, start_response):
#	status = '200 OK'
#	output = 'Hello World!'
#	response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
#	start_response(status, response_headers)
#	return [output]
