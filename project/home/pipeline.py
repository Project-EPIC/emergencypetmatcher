from django.shortcuts import render_to_response, redirect
from django.contrib import messages
from django.template import RequestContext
from social_auth.backends.facebook import FacebookBackend
from social_auth.backends.twitter import TwitterBackend
from urllib import urlopen
from StringIO import StringIO
from django.forms.models import model_to_dict
from constants import HTML_SOCIAL_AUTH_FORM, URL_SOCIAL_AUTH_GET_DETAILS, URL_LOGIN, URL_SOCIAL_AUTH_COMPLETE
from home.models import UserProfile
from utils import print_error_msg, print_debug_msg, print_info_msg
from pprint import pprint
import settings, logger

#Used by social auth pipeline to get a username value when authenticate a social user for the first time
def redirect_to_form(backend, details, request, social_user, is_new, uid, user, *args, **kwargs):
    print_info_msg("at redirect_to_form")
    print_info_msg("user_dict: %s" % request.session.get("user_dict"))
    print_info_msg("user: %s" % user)
    print_info_msg("is_new: %s" % is_new)

    #Determine whether to show social detail form, or to return with a welcome.
    if not request.session.get('user_dict') and user is None:
        return redirect (URL_SOCIAL_AUTH_GET_DETAILS, backend=backend)

    if is_new == False and user != None:    
        messages.success(request, "Welcome, %s!" % user.username)

def setup_User_fields(backend, details, request, social_user, is_new, uid, user, *args, **kwargs):
    print_info_msg("at home.pipeline.setup_User_fields")
    #Get the User attributes from the session.
    if is_new == True:
        user_dict = request.session.get("user_dict")
        return {"user_dict":user_dict}
    return {}

# Get profile pictures from social accounts
# http://www.tryolabs.com/Blog/2012/02/13/get-user-data-using-django-social-auth/
# http://stackoverflow.com/questions/10843878/django-social-auth-how-to-get-the-profile-pic-of-facebook-and-save-it-in-media
def set_profile_image(backend, details, request, response, social_user, is_new, uid, user, *args, **kwargs):
    print_info_msg("At home.pipeline.set_profile_image")
    user_dict = request.session.get("user_dict")
    #pprint(user_dict)
    print_debug_msg("is new user: %s " % is_new)

    #Set the Profile Image iff the user/userprofile is_new (True).
    if is_new == True:
        if backend.__class__ == FacebookBackend:
            url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
        elif backend.__class__ == TwitterBackend:
            url = response.get('profile_image_url', '').replace('_normal', '')

        #Get UserProfile safely
        profile = UserProfile.get_UserProfile(profile_id=user.get_profile().id)

        #This should never happen, but if it does, then redirect to Login with error message.
        if profile == None:
            print_error_msg("Could not find UserProfile!")
            messages.error(response, "Oops! Something went awry with your profile! Give us some time to fix it, and try again later.")
            return redirect (URL_LOGIN)

        #Setup the User with modified attributes including image path.
        profile.user.username = user_dict ["username"]
        profile.user.email = user_dict ["email"]
        profile.user.first_name = user_dict ["first_name"]
        profile.user.last_name = user_dict ["last_name"]
        img_path = StringIO(urlopen(url).read())
        profile.set_images(img_path)
        profile.user.save()

    return {}

def create_user_log(backend, details, response, social_user, uid, user, *args, **kwargs):
    print_info_msg("At home.pipeline.create_user_log")
    userprofile = user.get_profile()
    if logger.log_exists(userprofile) == False:
        logger.log_activity(logger.ACTIVITY_ACCOUNT_CREATED, userprofile)
    logger.log_activity(logger.ACTIVITY_LOGIN, user.get_profile())
           








