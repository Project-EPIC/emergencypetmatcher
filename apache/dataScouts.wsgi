import os, sys

apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)

sys.path.append('/srv/dataScouts') 
sys.path.append('/Library/Python/2.7/site-packages/django/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'dataScouts.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

def application(environ, start_response):
    environ['PATH_INFO'] = environ['SCRIPT_NAME'] + environ['PATH_INFO']
    return _application(environ, start_response)