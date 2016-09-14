SOCIAL_AUTH_TWITTER_KEY        = 'X'
SOCIAL_AUTH_TWITTER_SECRET     = 'X'
SOCIAL_AUTH_FACEBOOK_KEY       = 'X'
SOCIAL_AUTH_FACEBOOK_SECRET    = 'X'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']

SOCIAL_AUTH_ERROR_KEY = 'social_errors'
SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_CREATE_USERS          = True
SOCIAL_AUTH_FORCE_RANDOM_USERNAME = False
SOCIAL_AUTH_ERROR_KEY             = 'socialauth_error'

FACEBOOK_EXTENDED_PERMISSIONS = ['email', 'first_name', 'last_name']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
  'locale': 'ru_RU',
  'fields': 'id, name, email'
}
# No permisson for email in Twitter, check this https://dev.twitter.com/discussions/4019

SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email']

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'home.pipeline.redirect_to_form',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'home.pipeline.setup_user_details',
)

# Twitter testing
TEST_TWITTER_USER = 'X'
TEST_TWITTER_PASSWORD = 'X'

# Facebook testing
TEST_FACEBOOK_USER = 'X'
TEST_FACEBOOK_PASSWORD = 'X'
TEST_DOMAIN = 'http://localhost:8000/'
