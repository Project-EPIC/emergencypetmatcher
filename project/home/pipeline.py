from django.http import HttpResponseRedirect
from django.contrib import messages
import logger


def redirect_to_form(*args, **kwargs):
    
    if (not kwargs['request'].session.get('saved_username')) and (kwargs.get('user') is None):
        return HttpResponseRedirect('/get_social_details/')
    else: 
        print "PROBLEM at redirect_to_form pipline function!"

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
from social_auth.backends.facebook import FacebookBackend
from social_auth.backends.twitter import TwitterBackend
from urllib import urlopen
import settings
def get_user_avatar(backend, details, response, social_user, uid, user, *args, **kwargs):
    url = None
    if backend.__class__ == FacebookBackend:
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
 
    elif backend.__class__ == TwitterBackend:
        url = response.get('profile_image_url', '').replace('_normal', '')
 
    if url:
        profile = user.get_profile()
        avatar = urlopen(url).read()
        file_path_name=settings.STATIC_URL+'images/profile_images/'+ str(user) + '.jpg'
        fout = open(file_path_name, "wb") #file_path_name is where to save the image
        fout.write(avatar)
        fout.close()
        file_name='/images/profile_images/'+ str(user) + '.jpg'
        profile.photo = file_name # depends on where you saved it
        profile.save()

def create_user_log(backend, details, response, social_user, uid, user, *args, **kwargs):
    userprofile = user.get_profile()
    if logger.log_exists(userprofile) == False:
        logger.log_activity(logger.ACTIVITY_ACCOUNT_CREATED, userprofile)
    logger.log_activity(logger.ACTIVITY_LOGIN, user.get_profile())
           
