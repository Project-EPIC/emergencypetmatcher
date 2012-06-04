TWITTER_CONSUMER_KEY        = 'ssl0g9FopCG1zsItjarBJg'
TWITTER_CONSUMER_SECRET     = 'eDRctXylxlXxHuFQqrLSXcRtTkY1CVMpZtdaM46Wg'
FACEBOOK_APP_ID             = '294682853930535'
FACEBOOK_API_SECRET         = '0106dd00c7a51e98fccbbd99e6b89db3'
GOOGLE_OAUTH2_CLIENT_ID     = ''
GOOGLE_OAUTH2_CLIENT_SECRET = ''

LOGIN_URL = 'epm/auth/'
LOGIN_REDIRECT_URL = '/epm/auth/done'
LOGIN_ERROR_URL = '/epm/auth/login-error/'

SOCIAL_AUTH_ERROR_KEY = 'social_errors'

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    'social_auth.context_processors.social_auth_by_name_backends',
)

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
