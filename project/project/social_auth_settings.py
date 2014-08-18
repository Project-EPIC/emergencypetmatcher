
SOCIAL_AUTH_TWITTER_KEY        = 'K42bozieypTgRCQgDqcJsQ'
SOCIAL_AUTH_TWITTER_SECRET     = 'XgYnjnsp0eyQgKOCNEJT8c1dETON3p5Uv6mopbAEI'
FACEBOOK_APP_ID             = '315409715220911'
FACEBOOK_API_SECRET         = '0d6dccfbd7f042c31a29904222df78a2'

SOCIAL_AUTH_ERROR_KEY = 'social_errors'
SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_CREATE_USERS          = True
SOCIAL_AUTH_FORCE_RANDOM_USERNAME = False
SOCIAL_AUTH_ERROR_KEY             = 'socialauth_error'
# SOCIAL_AUTH_CHANGE_SIGNAL_ONLY = True   #?????


FACEBOOK_EXTENDED_PERMISSIONS = ['email']
# No permisson for email in Twitter, check this https://dev.twitter.com/discussions/4019

SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email']

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    # 'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details',
    'home.pipeline.redirect_to_form',
)

# Twitter testing
TEST_TWITTER_USER = 'epicdatascouts'
TEST_TWITTER_PASSWORD = 'crowdsourcing'

# Facebook testing
# TEST_FACEBOOK_USER = 'epicdatascouts'
TEST_FACEBOOK_USER = '100004419938460@facebook.com'
TEST_FACEBOOK_PASSWORD = 'crowdsourcing'
TEST_DOMAIN = 'http://localhost:8000/'