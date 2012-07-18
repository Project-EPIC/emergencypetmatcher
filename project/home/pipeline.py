from django.http import HttpResponseRedirect


def redirect_to_form(*args, **kwargs):
    if not kwargs['request'].session.get('saved_username') and kwargs.get('user') is None:
        return HttpResponseRedirect('/form/')

def username(request, *args, **kwargs):
    if kwargs.get('user'):
        username = kwargs['user'].username
    else:
        username = request.session.get('saved_username')
    return {'username': username}


def redirect_to_form2(*args, **kwargs):
    if not kwargs['request'].session.get('saved_first_name'):
        return HttpResponseRedirect('/form2/')


def first_name(request, *args, **kwargs):
    if 'saved_first_name' in request.session:
        user = kwargs['user']
        user.first_name = request.session.get('saved_first_name')
        user.save()


# Get profile pictures from social accounts
# http://www.tryolabs.com/Blog/2012/02/13/get-user-data-using-django-social-auth/
# http://stackoverflow.com/questions/10843878/django-social-auth-how-to-get-the-profile-pic-of-facebook-and-save-it-in-media
from social_auth.backends.facebook import FacebookBackend
from social_auth.backends.twitter import TwitterBackend
from urllib import urlopen
import settings
def get_user_avatar(backend, details, response, social_user, uid,\
                    user, *args, **kwargs):
    url = None
    if backend.__class__ == FacebookBackend:
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
 
    elif backend.__class__ == TwitterBackend:
        url = response.get('profile_image_url', '').replace('_normal', '')
        #  https://github.com/omab/django-social-auth/issues/97
        # user.social_auth.get(provider='twitter').extra_data['profile_image_url']
 
    if url:
        profile = user.get_profile()
        avatar = urlopen(url).read()
        # file_path_name=settings.STATIC_URL+'images/profile_images/'+'pic_'+uid
        file_path_name=settings.STATIC_URL+'images/profile_images/'+ str(user) + '.jpg'
        #fileName = "media/mugshots/"+ str(user) + ".jpg"
        fout = open(file_path_name, "wb") #file_path_name is where to save the image
        fout.write(avatar)
        fout.close()
        # file_name='/images/profile_images/'+'pic_'+uid
        file_name='/images/profile_images/'+ str(user) + '.jpg'
        profile.photo = file_name # depends on where you saved it
        profile.save()
