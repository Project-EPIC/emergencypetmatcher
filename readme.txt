EmergencyPetMatcher (EPM) : No Place Like Home (NPLH) : Project README

Make sure you have the 'pip' package manager installed before continuing.
Make sure you have Django (1.3) installed before continuing.

Project Dependencies
======================================

1) Django-MongoDB-Engine (http://django-mongodb.org/topics/setup.html)
--- directly depends on Django-nonrel and djangotoolbox

	After you have Django installed, just do:

Django NonRel - Django 1.3 fork that supports non-relational databases like MongoDB and AppEngine
pip install hg+https://bitbucket.org/wkornewald/django-nonrel

Django ToolBox - extra tools needed for non-relational database support.
pip install hg+https://bitbucket.org/wkornewald/djangotoolbox

MongoDB Engine
pip install git+https://github.com/django-nonrel/mongodb-engine

DjangoSocialAuth - handles social network authentication
pip install django-social-auth

Existing settings should work.

Database Setup
=======================================
Database setup is pretty easy and should work already - the MongoDB store for NPLH is "nplh_db".

Django Configuration
=======================================
You will need to modify some settings in "settings.py", particularly the absolute file paths.  Change these to reflect whatever paths you set up, but you can likely just mirror what I did.

Apache/nginx configs + setup
========================================
I use both Apache and nginx web servers to host NPLH.  Nginx is the outward-facing web server and handles static content.  For any dynamic content (which is most of the app), a reverse proxy passes requests through to Apache on a different port.  Apache then picks up these requests and redirects to Django using mod_wsgi, which you can install as part of your regular Apache process.

Included in the server_configs directory are the configuration files for nginx and Apache that work on my server.  These will obviously need modification but you can probably use them as good starting points.

It is important to note that static content (like CSS, JS, and images) is served through nginx, meaning my URL structure usually retrieves these through a different top-level URL subdirectory than the application.  For example

http://sample.com/nplh <-- request hits nginx proxy through to port 8080, where Apache is listening
http://sample.com/nplh/static <-- nginx redirects this to /home/jbarron/public_html/sample.com/static, which itself is the root of a simple file-mapped directory. 

Here are some sample urls to help you understand the structure:

sample.com/nplh <- maps to -> Apache root <- maps to -> Root Django URL
sample.com/nplh/static/css/style.css <-> /home/myname/public_html/sitename/static/css/style.css
sample.com/nplh/reporting <-> Apache <-> Reporting view index

Basically, static urls redirect to a static file structure outside the Django project, and everything else gets mapped to Django URLs.

