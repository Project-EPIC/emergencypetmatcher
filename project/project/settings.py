# Django settings for project project.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*"]

DATABASES = {
    'default': {
        #'ENGINE':'django.db.backends.postgresql_psycopg2',     # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.  
        'ENGINE':'django.db.backends.sqlite3',     # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.  
        'NAME': 'epm_db',                      # Or path to database file if using sqlite3.
        'USER': 'epm_login',                      # Not used with sqlite3.
        'PASSWORD': '3m3rgEncY',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

#Absolute filesystem path to the project directory. Use for creating relative paths.
#PROJECT_ROOT = "/vagrant/project"
PROJECT_ROOT = "/Users/mbarrenecheajr/Documents/Development/code/epm/project"

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
#MEDIA_ROOT = '/vagrant/media/'
MEDIA_ROOT = "/Users/mbarrenecheajr/Documents/Development/code/epm/media/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
#MEDIA_URL = '/vagrant/media/'
MEDIA_URL = "/Users/mbarrenecheajr/Documents/Development/code/epm/media/"

if DEBUG == False:
    # Absolute path to the directory static files should be collected to.
    # Don't put anything in this directory yourself; store your static files
    # in apps' "static/" subdirectories and in STATICFILES_DIRS.
    # Example: "/home/media/media.lawrence.com/static/"
    STATIC_ROOT = '/vagrant/deployment/static/'
    # URL prefix for static files.
    # Example: "http://media.lawrence.com/static/"
    STATIC_URL = '/vagrant/deployment/static/' 
else:
    STATIC_ROOT = '/vagrant/static/'
    # URL prefix for static files.
    # Example: "http://media.lawrence.com/static/"
    STATIC_URL = '/vagrant/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2wmzko%to)il=3(6@0mf_qd8vwh!=%@uti4ml^w9z7rs&amp;xfc0e'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'project.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home',
    'socializing',
    'matching',
    'reporting',
    'verifying',
    'registration',
    'social.apps.django_app.default',
    'analysis',
    'south',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    
)

#Variable to specify location of redirection after a successful login
LOGIN_REDIRECT_URL = '/'
#Variable to specify location of login
LOGIN_URL = '/login'
#Variable to specify location of logout
LOGOUT_URL = '/'

#Variable that specifies the exact model representing the user profile for the auth.User model.
AUTH_PROFILE_MODULE = 'socializing.UserProfile'

ACCOUNT_ACTIVATION_DAYS = 1 # One-week activation window; you may, of course, use a different value.

'''Email Settings'''
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#Swap with the filebased email backend when testing.
# "django.core.mail.backends.filebased.EmailBackend"

#Email File Path - Used for testing email messages.
EMAIL_FILE_PATH =  PROJECT_ROOT + "email-test.txt"
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'emergencypetmatcher@gmail.com'
EMAIL_HOST_PASSWORD = 'h!5H_3m3rgEncY'
DEFAULT_FROM_EMAIL = "emergencypetmatcher@gmail.com"

RECAPTCHA_SERVER_SECRET = "6LfkHgITAAAAAF1RcPPIB4ydg-_19xFLmoKvEJIr"
RECAPTCHA_CLIENT_SECRET = "6LfkHgITAAAAANIuw-RwYMfOWEMBfeVll9nhrdKa"
RECAPTCHA_SITEVERIFY = "https://www.google.com/recaptcha/api/siteverify"

AUTHENTICATION_BACKENDS = (
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_ENABLED_BACKENDS = ('twitter')

DOMAIN_URL = 'http://www.emergencypetmatcher.com/'

try:
    from social_auth_settings import *
except:
    pass

