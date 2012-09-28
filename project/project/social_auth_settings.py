
TWITTER_CONSUMER_KEY        = 'ssl0g9FopCG1zsItjarBJg'
TWITTER_CONSUMER_SECRET     = 'eDRctXylxlXxHuFQqrLSXcRtTkY1CVMpZtdaM46Wg'

FACEBOOK_APP_ID             = '315409715220911'
FACEBOOK_API_SECRET         = '0d6dccfbd7f042c31a29904222df78a2'

SOCIAL_AUTH_ERROR_KEY = 'social_errors'

SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'


SOCIAL_AUTH_CREATE_USERS          = True
SOCIAL_AUTH_FORCE_RANDOM_USERNAME = False
# SOCIAL_AUTH_USER_MODEL            = 'home.UserProfile'
SOCIAL_AUTH_ERROR_KEY             = 'socialauth_error'
# SOCIAL_AUTH_CHANGE_SIGNAL_ONLY = True   #?????

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.associate.associate_by_email',
    'social_auth.backends.pipeline.misc.save_status_to_session',
    'home.pipeline.redirect_to_form',
    'home.pipeline.username',
    'social_auth.backends.pipeline.user.create_user',
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details',
    'social_auth.backends.pipeline.misc.save_status_to_session',
    'home.pipeline.get_user_avatar',
)

# Twitter testing
TEST_TWITTER_USER = 'epicdatascouts'
TEST_TWITTER_PASSWORD = 'crowdsourcing'

# Facebook testing
# TEST_FACEBOOK_USER = 'epicdatascouts'
TEST_FACEBOOK_USER = '100004419938460@facebook.com'
TEST_FACEBOOK_PASSWORD = 'crowdsourcing'

TEST_DOMAIN = 'http://localhost:8000'
