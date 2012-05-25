import os, sys
import site

apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)

site.addsitedir('/home/jbarron/nplh/lib/python2.7/site-packages')

#sys.path.append('/usr/lib/python2.7/site-packages/django-trunk/django')
sys.path.append('/home/jbarron/public_html/barronsoftware.com/nplh/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nplh.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
