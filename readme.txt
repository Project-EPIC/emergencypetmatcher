EmergencyPetMatcher (EPM) : No Place Like Home (NPLH) : Project README

This document is primarily for developers, designers, and administrators of the EPM system.

===================== Development Environment Setup =====================

- Make sure that you have the following installed on your development machine before continuing:
	- Python (2.7)
	- Pip (2.7)
	- Django (1.4)
	- git (1.7) (version control)

--------------------- Project Technologies --------------------- 

The following must be installed in order to set up the development environment for the EPM Django Project:

1) DjangoSocialAuth - handles social network authentication
pip install django-social-auth

2) mod_wsgi - WSGI module that allows Apache to run Python projects
download and install: http://code.google.com/p/modwsgi/

Existing settings should work.

--------------------- Database Setup --------------------- 

Database setup is pretty easy and should work already - the MongoDB store for EPM is "epm_db".

--------------------- Django Configuration --------------------- 

You will need to modify some settings in "settings.py", particularly the absolute file paths.  Change these to reflect whatever paths you set up, but you can likely just mirror what I did.

---------------------  Apache and nginx --------------------- 

Apache and nginx are web servers that together host NPLH.  Nginx is the outward-facing web server and handles static content. For any dynamic content (which is most of the app), a reverse proxy passes requests through to Apache on a different port.  Apache then picks up these requests and redirects to Django using mod_wsgi, which you have already installed.

Included in the server_configs directory are the configuration files (server_configs/josh/apache_config and server_config/josh/nginx_config) for nginx and Apache that work on my server.  These will obviously need modification but you can probably use them as good starting points.

It is important to note that static content (like CSS, JS, and images) is served through nginx, meaning my URL structure usually retrieves these through a different top-level URL subdirectory than the application.  For example:

http://sample.com/nplh <-- request hits nginx proxy through to port 8080, where Apache is listening
http://sample.com/nplh/static <-- nginx redirects this to /home/jbarron/public_html/sample.com/static, which itself is the root of a simple file-mapped directory. 

Here are some sample urls to help you understand the structure:

sample.com/nplh <- maps to -> Apache root <- maps to -> Root Django URL
sample.com/nplh/static/css/style.css <-> /home/myname/public_html/sitename/static/css/style.css
sample.com/nplh/reporting <-> Apache <-> Reporting view index

Basically, static urls redirect to a static file structure outside the Django project, and everything else gets mapped to Django URLs.

