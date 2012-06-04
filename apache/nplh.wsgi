import os, sys
import site

#This is the apache configuration folder path where the mod_wsgi script lives. It should be outside of the project directory.
apache_folder = os.path.dirname(__file__)

#This is the EPM workspace directory path (root directory) of the entire EPM project. One of its children should be the project directory.
epm_folder = os.path.dirname(apache_folder)

#This is the project directory path where the Django project and its apps should live.
project = epm_folder + '/nplh'

#We append the EPM directory path to SYS PATH.
sys.path.append(epm_folder)

#We need to make sure we add in all of our local Python modules here.
site.addsitedir('/home/jbarron/nplh/lib/python2.7/site-packages')

#sys.path.append('/usr/lib/python2.7/site-packages/django-trunk/django')
sys.path.append('/home/jbarron/public_html/barronsoftware.com/nplh/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'nplh.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
