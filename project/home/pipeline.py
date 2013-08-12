from django.shortcuts import render_to_response, redirect
from django.contrib import messages
from social_auth.backends.facebook import FacebookBackend
from social_auth.backends.twitter import TwitterBackend
from urllib import urlopen
from constants import URL_SOCIAL_AUTH_GET_DETAILS, URL_LOGIN
from home.models import UserProfile
from utils import print_error_msg, print_debug_msg, print_info_msg
import settings, logger

def redirect_to_form(*args, **kwargs):
    return redirect(URL_SOCIAL_AUTH_GET_DETAILS)

    print_debug_msg(kwargs)
    request = kwargs.get("request")
    user = kwargs.get("user")
    if (request.session.get('saved_username') is None) and (user is None):
        return redirect(URL_SOCIAL_AUTH_GET_DETAILS)
    else: 
        messages.error(request, "Oops, Something went awry with your profile! Give us some time to fix it, and try again later.")
        print_error_msg ("PROBLEM at redirect_to_form pipline function!")

def username(request, *args, **kwargs):
    if kwargs.get('user'):
        username = kwargs['user'].username
    else:
        username = request.session.get('saved_username')
    return {'username': username}

def email(request, *args, **kwargs):
    if kwargs.get('user'):
        email = kwargs['user'].email
    else:
        email = request.session.get('saved_email')
    return {'email': email}


# Get profile pictures from social accounts
# http://www.tryolabs.com/Blog/2012/02/13/get-user-data-using-django-social-auth/
# http://stackoverflow.com/questions/10843878/django-social-auth-how-to-get-the-profile-pic-of-facebook-and-save-it-in-media
def set_profile_image(backend, details, response, social_user, uid, user, *args, **kwargs):
    if backend.__class__ == FacebookBackend:
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
 
    elif backend.__class__ == TwitterBackend:
        url = response.get('profile_image_url', '').replace('_normal', '')

    #Get UserProfile
    profile = UserProfile.get_UserProfile(user.get_profile().id)

    #This should never happen, but if it does, then redirect to Login with error message.
    if profile == None:
        print_error_msg("Could not find UserProfile!")
        messages.error(response, "Oops! Something went awry with your profile! Give us some time to fix it, and try again later.")
        return redirect (URL_LOGIN)

    #Setup the image path.
    img_path = urlopen(url).read()
    profile.set_images(img_path)

def create_user_log(backend, details, response, social_user, uid, user, *args, **kwargs):
    userprofile = user.get_profile()
    if logger.log_exists(userprofile) == False:
        logger.log_activity(logger.ACTIVITY_ACCOUNT_CREATED, userprofile)
    logger.log_activity(logger.ACTIVITY_LOGIN, user.get_profile())
           








