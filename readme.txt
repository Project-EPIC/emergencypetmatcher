EmergencyPetMatcher (EPM) : No Place Like Home (NPLH) : Project README

This document is primarily for developers, designers, and administrators of the EPM system.

===================== Development Environment Setup =====================

- Make sure that you have the following installed on your development machine before continuing:
	- Python
	- Apache (2.2)
	- nginx (1.2)
	- mod_wsgi (3.3)
	- pip
	- gcc
	- Django (1.4.1)
	- git (version control)
	- hg (Mercurial is used for downloading other essential packages)

--------------------- Project Technologies --------------------- 

The following must be installed in order to set up the development environment for the EPM Django Project:

1) django-social-auth - handles social network authentication
[sudo pip install django-social-auth]

2) django-registration - handles account registration and activation, and verification emails.
[sudo pip install django-registration]

3) mod_wsgi - WSGI module that allows Apache to run Python projects
hg clone https://code.google.com/p/modwsgi/

4) Lipsum 

5) Selenium

6) PIL
	- Please set up these files to enable JPEG support: sudo apt-get install libjpeg libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev

Existing settings should work.

--------------------- Database Setup --------------------- 


--------------------- Django Configuration --------------------- 

You will need to modify some settings in "settings.py", particularly the absolute file paths.  Change these to reflect whatever paths you set up, but you can likely just mirror what I did.

---------------------  Server Configuration (Apache and Nginx) --------------------- 

[Apache]

	$	sudo apachectl start (starts the server)
	$	sudo apachectl stop (stops the server)
	$	sudo apachectl reload (restarts the server)

[Nginx]

	Nginx is the front-facing web server for handling static content for the EPM application.

	$ 	sudo nginx (start the server)
	$	sudo nginx -s stop (stop the server)
	$	sudo nginx -s reload (restart the server)

Apache and nginx are web servers that together host EPM.  Nginx is the outward-facing web server and handles static content. For any dynamic content (which is most of the app), a reverse proxy passes requests through to Apache on a different port.  Apache then picks up these requests and redirects to Django using mod_wsgi, which you have already installed.

Included in the server_configs directory are the configuration files (server_configs/josh/apache_config and server_config/josh/nginx_config) for nginx and Apache that work on my server.  These will obviously need modification but you can probably use them as good starting points.

It is important to note that static content (like CSS, JS, and images) is served through nginx, meaning my URL structure usually retrieves these through a different top-level URL subdirectory than the application.  For example:

http://sample.com/nplh <-- request hits nginx proxy through to port 8080, where Apache is listening
http://sample.com/nplh/static <-- nginx redirects this to /home/jbarron/public_html/sample.com/static, which itself is the root of a simple file-mapped directory. 

Here are some sample urls to help you understand the structure:

sample.com/nplh <- maps to -> Apache root <- maps to -> Root Django URL
sample.com/nplh/static/css/style.css <-> /home/myname/public_html/sitename/static/css/style.css
sample.com/nplh/reporting <-> Apache <-> Reporting view index

Basically, static urls redirect to a static file structure outside the Django project, and everything else gets mapped to Django URLs.

