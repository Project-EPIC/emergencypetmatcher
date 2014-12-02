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
from pprint import pprint
from constants import *
from utilities.utils import *
import settings

#Used by social auth pipeline to get a username value when authenticate a social user for the first time
@partial
def redirect_to_form(strategy, backend, uid, response, details, user=None, is_new=False, *args, **kwargs):
    print_info_msg("at redirect_to_form")
    # print_info_msg("strategy: %s" % strategy.__dict__)
    # print_info_msg("request: %s" % strategy.request.__dict__)
    # print_info_msg("response: %s" % response)
    # print_info_msg("backend: %s" % backend.__dict__)
    print_info_msg("details: %s" % details)
    print_info_msg("user: %s" % user)
    print_info_msg("is_new: %s" % is_new)
    request = strategy.request

    if is_new == True:   
        pic_url = None
        # pprint(response)            

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
                                                                    "consent_form_minor_text":CONSENT_FORM_MINOR_TEXT,
                                                                    "consent_form_adult_text":CONSENT_FORM_ADULT_TEXT }, RequestContext(request))

            details["username"] = username = request.POST.get("username")
            details["email"] = email = request.POST.get("email")
            details["first_name"] = first_name = request.POST.get("first_name")
            details["last_name"] = last_name = request.POST.get("last_name")
            details["minor"] = is_minor(request.POST.get("date_of_birth"))
            details["date_of_birth"] = request.POST.get("date_of_birth")
            details["guardian_email"] = request.POST.get("guardian_email")
            details["pic_url"] = pic_url
            print_info_msg("New Details: %s" % details)

        # If the user has logged in for the first time as facebook or twitter user, get details.
        else:
            return render_to_response(HTML_SOCIAL_AUTH_FORM, {  'username':details['username'],
                                                                'first_name':details['first_name'], 
                                                                'last_name':details['last_name'], 
                                                                'email':details['email'], 
                                                                "pic_url": pic_url,
                                                                "consent_form_minor_text":CONSENT_FORM_MINOR_TEXT,
                                                                "consent_form_adult_text":CONSENT_FORM_ADULT_TEXT }, RequestContext(request))
    elif user.is_active == True:
        messages.success(request, "Welcome, %s!" % user.username)
    else:
        messages.error(request, "Sorry, you haven't fully activated your account yet!")
        return redirect(URL_HOME)

@partial
def setup_user_details(strategy, backend, uid, response, details, user=None, is_new=False, *args, **kwargs):
    print_info_msg("at setup_user_details")
    request = strategy.request

    if is_new == True:
        print_info_msg("User: %s" % user)
        print_info_msg("Details: %s" % details)

        if details["minor"] == True:
            print_info_msg("User is a minor...")
            #User is not supposed to be activated because of minor status.
            user.is_active = False

            #Create a RegistrationProfile object, populate the potential User object, and be ready for activation.
            registration_profile = RegistrationProfile.objects.create_profile(user)
            profile = user.userprofile
            profile.is_minor = True
            profile.guardian_email = details["guardian_email"]
            profile.guardian_activation_key = create_sha1_hash(details["username"])

            #Send an email to the minor.
            registration_profile.send_activation_email(Site.objects.get_current())

            #Send an email to the guardian with activation key.
            email_subject = render_to_string(TEXTFILE_EMAIL_GUARDIAN_SUBJECT, {})
            email_body = render_to_string(TEXTFILE_EMAIL_GUARDIAN_BODY, 
                {   "participant_email": details["email"], 
                    "guardian_activation_key": profile.guardian_activation_key,
                    "consent_form_guardian_text": CONSENT_FORM_GUARDIAN_TEXT,
                    "site": Site.objects.get_current() })
            
            send_mail(email_subject, email_body, None, [profile.guardian_email])
            print_info_msg ("(SOCIAL AUTH): RegistrationProfile now created for inactive user %s" % user)
            messages.success(request, "Thanks for registering for EPM! Look for an account activation link sent to both you and your parent/guardian email address.")   
        else:
            messages.success(request, "Welcome to EPM, %s! You can now login using Twitter!" % details["username"])     

        user.first_name = details["first_name"]
        user.last_name = details["last_name"]
        user.username = details["username"]
        user.email = details["email"]
        user.save()

        #We have retrieved a picture link from Facebook OR from Twitter, otherwise raise Http404.
        if backend.name == "twitter":
            profile = user.userprofile
            img_path = StringIO(urlopen(details["pic_url"]).read())
            profile.set_images(img_path)
            profile.set_date_of_birth(details["date_of_birth"])
            profile.social_profile = True
            profile.save()

        if profile.is_minor == True:   
            return redirect(URL_HOME)








