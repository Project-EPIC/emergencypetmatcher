# Django settings for project project.
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd14kwqaf8km%hn*yb453lnhez!!t^80dwpxde8gu%#9_!lzd5!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ADMINS = (
    ('X', 'X'),
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
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Denver'

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

STATIC_ROOT = BASE_DIR + "/static/"
# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'


# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = BASE_DIR + "/media/"

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = "/media/"

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder'
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2wmzko%to)il=3(6@0mf_qd8vwh!=%@uti4ml^w9z7rs&amp;xfc0e'

PIPELINE = {
    "PIPELINE_ENABLED": not DEBUG,
    "JAVASCRIPT" : {
        'vendor':{
            'source_filenames':(
                'home/js/jquery-1.9.1.min.js',
                'home/js/bootstrap-datepicker.js',
                'reporting/js/select2.full.min.js',
                'reporting/js/leaflet.js',
                'reporting/js/l.control.geosearch.js',
                'reporting/js/l.geosearch.provider.google.js',
                'home/js/jquery-imagesloaded.js',
                'home/js/jquery-rotate.min.js',
                'home/js/jquery-wookmark.js',
                'home/js/jquery.zoom.min.js',
            ),
            'output_filename': 'js/vendor.js'
        }
    },
    "STYLESHEETS": {
        "vendor": {
            'source_filenames': (
                'home/css/bootstrap.min.css',
                'home/css/datepicker.css',
                'reporting/css/leaflet.css',
                'reporting/css/select2.min.css',
                'reporting/css/l.geosearch.css',
                'reporting/css/select2-bootstrap.css'
            ),
            'output_filename': 'css/vendor.css',
            'variant':'datauri',
        }
    }
}

PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    }
]

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
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
    'pipeline',
    'social.apps.django_app.default',
    'analysis',
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

TEST_RUNNER = 'rainbowtests.test.runner.RainbowDiscoverRunner'

#Variable that specifies the exact model representing the user profile for the auth.User model.
AUTH_PROFILE_MODULE = 'socializing.UserProfile'

ACCOUNT_ACTIVATION_DAYS = 1 # One-week activation window; you may, of course, use a different value.

#Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#Email File Path - Used for testing email messages.
EMAIL_FILE_PATH =  BASE_DIR + "email-test.txt"

#May need to retrieve separate RECAPTCHA codes.
RECAPTCHA_SERVER_SECRET = "6LfkHgITAAAAAF1RcPPIB4ydg-_19xFLmoKvEJIr"
RECAPTCHA_CLIENT_SECRET = "6LfkHgITAAAAANIuw-RwYMfOWEMBfeVll9nhrdKa"
RECAPTCHA_SITEVERIFY = "https://www.google.com/recaptcha/api/siteverify"

TEST_RECAPTCHA_CLIENT_SECRET="6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
TEST_RECAPTCHA_SERVER_SECRET="6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_ENABLED_BACKENDS = ('twitter')

DOMAIN_URL = 'http://www.emergencypetmatcher.com/'

try:
    from social_auth_settings_real import *
    from email_settings_real import *
except:
    pass
