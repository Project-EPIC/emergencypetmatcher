import os, sys
import site
import django.core.handlers.wsgi

#Path Constants (relative to project directory) - edit this to reflect changes in project WSGI script.
PROJECT_NAME = '/project'
SITE_PACKAGES = '/lib/python2.7/site-packages'

#This is the apache configuration folder path where the mod_wsgi script lives. It should be outside of the project directory.
apache_folder = os.path.dirname(__file__)

#This is the EPM workspace directory path (root directory) of the entire EPM project. One of its children should be the project directory.
workspace = os.path.dirname(apache_folder)

#This is the project directory path where the Django project and its apps should live.
project = workspace + PROJECT_NAME

#We append the EPM directory path to SYS PATH.
sys.path.append(workspace)
#sys.path.append('/home/jbarron/public_html/barronsoftware.com/nplh/')

#We need to make sure we add in all of our local Python modules here.
site.addsitedir(workspace + SITE_PACKAGES)

#Some general important settings.
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
application = django.core.handlers.wsgi.WSGIHandler()

#This is how you can test if its working. You should get a "Hello World!" to the browser screen.
#def application(environ, start_response):
#	status = '200 OK'
#	output = 'Hello World!'
#	response_headers = [('Content-type', 'text/plain'), ('Content-Length', str(len(output)))]
#	start_response(status, response_headers)
#	return [output]
