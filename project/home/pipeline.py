from django.shortcuts import render_to_response, redirect
from django.contrib import messages
from django.template import RequestContext
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.models import User
from registration.models import RegistrationProfile
from urllib import urlopen
from StringIO import StringIO
from django.template.loader import render_to_string
from django.forms.models import model_to_dict
from home.constants import HTML_SOCIAL_AUTH_FORM, URL_SOCIAL_AUTH_GET_DETAILS, URL_LOGIN, URL_SOCIAL_AUTH_COMPLETE
from socializing.models import UserProfile, UserProfileForm
from social.pipeline.partial import partial
from pprint import pprint
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from requests import request, HTTPError
from django.core.files.base import ContentFile
from constants import *
from utilities.utils import *
import settings, ipdb

#Used by social auth pipeline to get a username value when authenticate a social user for the first time
@partial
def redirect_to_form(strategy, backend, uid, response, details, user=None, is_new=False, *args, **kwargs):
    request = strategy.request
    if is_new == True:
        if backend.name == "twitter":
            pic_url = response.get('profile_image_url').replace("_normal", "")
        elif backend.name == "facebook":
            pic_url = "http://graph.facebook.com/%s/picture?type=large" % response["id"]

        if request.method == 'GET': #If this is the first time user is using social auth...
            details["username"] = details["username"].strip().replace(" ", "")
            form = UserProfileForm(initial=details)
            form.fields.pop("password1")
            form.fields.pop("password2")
            return render_to_response(HTML_SOCIAL_AUTH_FORM, {
                'form': form,
                "pic_url": pic_url,
                "RECAPTCHA_CLIENT_SECRET": settings.RECAPTCHA_CLIENT_SECRET,
                "consent_form_minor_text":CONSENT_FORM_MINOR_TEXT,
                "consent_form_adult_text":CONSENT_FORM_ADULT_TEXT
            }, RequestContext(request))

        if request.method == 'POST': #If the first-time user submits the form...
            form = UserProfileForm(request.POST, request.FILES)
            success, message = UserProfile.check_registration(post_obj=request.POST, userprofileform=form, social=True)
            if success == False:
                messages.error(request, message)
                form.fields.pop("password1")
                form.fields.pop("password2")
                return render_to_response(HTML_SOCIAL_AUTH_FORM, {
                    'form': form,
                    'pic_url':pic_url,
                    "RECAPTCHA_CLIENT_SECRET": settings.RECAPTCHA_CLIENT_SECRET,
                    "consent_form_minor_text":CONSENT_FORM_MINOR_TEXT,
                    "consent_form_adult_text":CONSENT_FORM_ADULT_TEXT
                }, RequestContext(request))

            details["username"] = username = request.POST.get("username")
            details["email"] = email = request.POST.get("email")
            details["first_name"] = first_name = request.POST.get("first_name")
            details["last_name"] = last_name = request.POST.get("last_name")
            details["minor"] = is_minor(request.POST.get("dob"))
            details["dob"] = request.POST.get("dob")
            details["guardian_email"] = request.POST.get("guardian_email")

            if bool(request.FILES): #Need to check if file was uploaded.
                details["pic_url"] = request.FILES.get("img_path")
            else:
                details["pic_url"] = pic_url
            print_info_msg("New Details: %s" % details)

    elif user.is_active == True:
        messages.success(request, "Welcome, %s!" % user.username)
    else:
        messages.error(request, "Sorry, you haven't fully activated your account yet!")
        return redirect(URL_HOME)

@partial
def setup_user_details(strategy, backend, uid, response, details, user=None, is_new=False, *args, **kwargs):
    request = strategy.request
    if is_new == True:
        if details["minor"] == True:
            user.is_active = False #User is not supposed to be activated because of minor status.
            registration_profile = RegistrationProfile.objects.create_profile(user)
            profile = user.userprofile
            profile.is_minor = True
            profile.guardian_email = details["guardian_email"]
            profile.guardian_activation_key = create_sha1_hash(details["username"])
            #Send an email to the minor.
            registration_profile.send_activation_email(Site.objects.get_current())
            #Send an email to the guardian with activation key.
            email_subject = render_to_string(TEXTFILE_EMAIL_GUARDIAN_SUBJECT, {})
            email_body = render_to_string(TEXTFILE_EMAIL_GUARDIAN_BODY, {
                "participant_email": details["email"],
                "guardian_activation_key": profile.guardian_activation_key,
                "consent_form_guardian_text": CONSENT_FORM_GUARDIAN_TEXT,
                "site": Site.objects.get_current()
            })

            send_email(email_subject, email_body, None, [profile.guardian_email])
            print_info_msg ("(SOCIAL AUTH): RegistrationProfile now created for inactive user %s" % user)

        user.first_name = details["first_name"]
        user.last_name = details["last_name"]
        user.username = details["username"]
        user.email = details["email"]
        user.save()

        if type(details["pic_url"]) == InMemoryUploadedFile:
            img_path = details["pic_url"]
        else:
            img_path = StringIO(urlopen(details["pic_url"]).read())

        profile = user.userprofile
        profile.set_images(img_path, save=True, rotation=request.POST.get("img_rotation"))
        profile.set_date_of_birth(details["dob"])
        profile.social_profile = True
        profile.save()

        if profile.is_minor == True:
            messages.success(request, "Thanks for registering for EPM! Look for an account activation link sent to both you and your parent/guardian email address.")
        else:
            messages.success(request, "Welcome to EmergencyPetMatcher, %s!" % details["username"])
