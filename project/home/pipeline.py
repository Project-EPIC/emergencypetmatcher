from django.shortcuts import render_to_response, redirect
from django.contrib import messages
from django.template import RequestContext
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from registration.models import RegistrationProfile
from urllib import urlopen
from StringIO import StringIO
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from home.constants import HTML_SOCIAL_AUTH_FORM, URL_SOCIAL_AUTH_GET_DETAILS, URL_LOGIN, URL_SOCIAL_AUTH_COMPLETE
from socializing.models import UserProfile
from social.pipeline.partial import partial
from utilities import logger
from pprint import pprint
from home.constants import *
from utilities.utils import *
import settings

#Used by social auth pipeline to get a username value when authenticate a social user for the first time
@partial
def redirect_to_form(strategy, backend, uid, request, response, details, user=None, is_new=False, *args, **kwargs):
    print_info_msg("at redirect_to_form")
    print_info_msg("backend: %s" % backend.__dict__)
    print_info_msg("details: %s" % details)
    print_info_msg("user: %s" % user)
    print_info_msg("is_new: %s" % is_new)
    pic_url = None
    # pprint(response)

    #We have retrieved a picture link from Twitter.
    if backend.name == "twitter":
        pic_url = response.get('profile_image_url').replace("_normal", "")

    #If the first-time user submits the form... 
    if request.method == 'POST':
        success, message = UserProfile.check_registration(post_obj=request.POST)

        if success == False:
            messages.error(request, message)
            return render_to_response(HTML_SOCIAL_AUTH_FORM,{   'username':details['username'],
                                                                'first_name':details['first_name'], 
                                                                'last_name':details['last_name'], 
                                                                'email':details['email'], 
                                                                'pic_url':pic_url, 
                                                                "tos_minor_text":TOS_MINOR_TEXT,
                                                                "tos_adult_text":TOS_ADULT_TEXT }, RequestContext(request))

        kwargs["username"] = username = request.POST.get("username")
        kwargs["email"] = email = request.POST.get("email")
        kwargs["first_name"] = first_name = request.POST.get("first_name")
        kwargs["last_name"] = last_name = request.POST.get("last_name")
        kwargs["minor"] = minor = is_minor(request.POST.get("date_of_birth"))
        kwargs["pic_url"] = pic_url


        #If this user is a minor, activation is necessary: save some extra information to be checked during activation.
        if minor == True:
            #Create a RegistrationProfile object, populate the potential User object, and be ready for activation.
            user = RegistrationProfile.objects.create_inactive_user(username, email, request.POST.get("password1"), Site.objects.get_current())
            profile = user.get_profile()            
            profile.is_minor = True
            profile.guardian_email = request.POST.get("guardian_email")
            profile.guardian_activation_key = create_sha1_hash(user.username)

            #Send an email to the guardian with activation key.
            email_body = render_to_string(TEXTFILE_EMAIL_GUARDIAN_BODY, 
                {   "participant_email": email, 
                    "guardian_activation_key": profile.guardian_activation_key,
                    "site": Site.objects.get_current() })
            email_subject = render_to_string(TEXTFILE_EMAIL_GUARDIAN_SUBJECT, {})
            send_mail(email_subject, email_body, None, [profile.guardian_email])
            print_info_msg ("(SOCIAL AUTH): RegistrationProfile now created for inactive user %s" % user)
            messages.success(request, "Thanks for registering for EPM! Look for an account activation link sent to both you and your parent/guardian email address.")
            return redirect(URL_HOME)
        else:
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            profile = user.get_profile()
            messages.success(request, "Welcome to EPM, %s! You can now login using Twitter!" % username)

    # If the user has logged in for the first time as facebook or twitter user, get details.
    else:
        return render_to_response(HTML_SOCIAL_AUTH_FORM, {  'username':details['username'],
                                                            'first_name':details['first_name'], 
                                                            'last_name':details['last_name'], 
                                                            'email':details['email'], 
                                                            'pic_url':pic_url, 
                                                            "tos_minor_text":TOS_MINOR_TEXT,
                                                            "tos_adult_text":TOS_ADULT_TEXT }, RequestContext(request))

@partial
def setup_user_details(strategy, backend, uid, request, response, details, user=None, is_new=False, *args, **kwargs):
    print_info_msg("at setup_user_details")
    pprint(user)
    pprint(details)
    pprint(kwargs)
    profile = user.get_profile()
    user.first_name = details["first_name"]
    user.last_name = details["last_name"]
    user.username = details["username"]
    user.email = details["email"]
    user.save()

    #We have retrieved a picture link from Facebook OR from Twitter, otherwise raise Http404.
    if backend.name == "twitter":
        pic_url = response.get('profile_image_url').replace("_normal", "")    
        img_path = StringIO(urlopen(details["pic_url"]).read())
        profile.set_images(img_path)
        profile.save()    

def create_user_log(backend, details, response, social_user, uid, user, *args, **kwargs):
    print_info_msg("At home.pipeline.create_user_log")
    userprofile = user.get_profile()
    if logger.log_exists(userprofile) == False:
        logger.log_activity(logger.ACTIVITY_ACCOUNT_CREATED, userprofile)
    logger.log_activity(logger.ACTIVITY_LOGIN, user.get_profile())
           








