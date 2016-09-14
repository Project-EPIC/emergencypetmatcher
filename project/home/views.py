from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import *
from django.contrib.sites.models import Site
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import JsonResponse
from django.contrib.messages.api import get_messages
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.http import Http404
from urllib import urlopen
from StringIO import StringIO
from django.core import mail
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.timezone import now as datetime_now
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db.models import Count
from registration.models import RegistrationProfile
from registration.forms import RegistrationFormTermsOfService
from datetime import datetime
from models import Activity
from socializing.models import UserProfile, UserProfileForm
from reporting.models import PetReport
from matching.models import PetMatch
from verifying.models import PetReunion, PetMatchCheck
from constants import *
from reporting.constants import NUM_PETREPORTS_HOMEPAGE, NUM_BOOKMARKS_HOMEPAGE
from matching.constants import NUM_PETMATCHES_HOMEPAGE
from utilities.utils import *
from pprint import pprint
import oauth2 as oauth, json, ipdb, random, urllib, hashlib, random, re, project.settings, registration

def home (request):
    filters = {k:v for k, v in request.GET.iteritems() if (k in ["breed", "status", "pet_type", "pet_name", "event_tag"])}
    return render_to_response(HTML_HOME, filters, RequestContext(request))

def get_activities(request):
    if request.is_ajax() == True:
        page = request.GET.get("page") or 0

        #Let's populate the activity feed based upon whether the user is logged in.
        if request.user.is_authenticated() == True:
            print_info_msg ("get_activities(): Authenticated User - recent activities...")
            current_userprofile = request.user.userprofile

        activities = Activity.get_Activities_for_feed(page=page, since_date=None, userprofile=None)
        #Zip it up in JSON and ship it out as an HTTP Response.
        activities = [{
            "activity"          : activity.activity,
            "date_posted"       : activity.date_posted.ctime(),
            "profile"           : activity.userprofile.to_DICT(),
            "source"            : activity.get_source_DICT(),
            "text"              : activity.text
        } for activity in activities]

        return JsonResponse({"activities":activities}, safe=False)
    else:
        print_error_msg ("Request for get_activities not an AJAX request!")
        raise Http404

@login_required
def get_bookmarks(request):
    if request.is_ajax() == True:
        page = int(request.GET["page"])
        up = request.user.userprofile
        bookmarks = up.bookmarks_related.all()
        #Get the bookmark count for pagination purposes.
        bookmarks_count = len(bookmarks)
        #Now get just a page of bookmarks if page # is available.
        bookmarks = get_objects_by_page(bookmarks, page, limit=NUM_BOOKMARKS_HOMEPAGE)
        #Zip it up in JSON and ship it out as an HTTP Response.
        bookmarks = [{
            "ID"                    : pr.id,
            "proposed_by_username"  : pr.proposed_by.user.username,
            "pet_name"              : pr.pet_name,
            "pet_type"              : pr.pet_type,
            "status"                : pr.status,
            "img_path"              : pr.thumb_path.name
        } for pr in bookmarks]

        return JsonResponse({"bookmarks_list":bookmarks, "count":len(bookmarks), "total_count": bookmarks_count}, safe=False)
    else:
        raise Http404

def login_User(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user != None:
            if user.is_active == True:
                userprofile = user.userprofile

                login(request, user)
                messages.success(request, 'Welcome, %s!' % (username))
                Activity.log_activity("ACTIVITY_LOGIN", user.userprofile)
                next_url = request.GET.get('next', URL_HOME)

                if "//" in next_url and re.match(r'[^\?]*//', next_url):
                    next_url = settings.LOGIN_REDIRECT_URL
                return redirect(next_url)

            else:
                messages.error(request, "You haven't activated your account yet. Please check your email.")
        else:
            messages.error(request, 'Invalid Login credentials. Please try again.')

    next_path = request.GET.get('next', URL_HOME)
    form = AuthenticationForm()
    return render_to_response(HTML_LOGIN, {'form':form}, RequestContext(request, {'next': next_path}))


@login_required
def logout_User(request):
    # Update last_logout date field
    user = get_object_or_404(UserProfile, pk=request.user.userprofile.id)
    user.last_logout = datetime.now()
    user.save()

    Activity.log_activity("ACTIVITY_LOGOUT", request.user.userprofile)
    messages.success(request, "See you next time!")
    logout(request)
    return redirect(URL_HOME)

def registration_activate (request, activation_key=None, backend=None):
    print_info_msg ("Activation Key: %s" % activation_key)
    #Does the activation key exist within a RegistrationProfile?
    #(i.e. is somebody actually trying to activate an account or resurrect an old activation link?)
    try:
        rp = RegistrationProfile.objects.get(activation_key=activation_key)
        profile = rp.user.userprofile

    except RegistrationProfile.DoesNotExist:
        messages.error(request, "This account has already been activated!")
        return redirect(URL_HOME)

    #Need to check if user is a minor and if parent/guardian consented.
    if profile.is_minor == False or profile.guardian_consented == True:
        if rp.activation_key_expired() == False:
            activated_user = RegistrationProfile.objects.activate_user(activation_key)
            print_info_msg ("RegistrationProfile now activated for active user %s" % activated_user)
            return redirect (URL_ACTIVATION_COMPLETE)
        else:
            rp.delete()
            messages.error(request, "Activation has expired! Please re-register your account.")
            return redirect (URL_HOME)
    else:
        messages.error(request, "Your Parent/Guardian has not yet verified your account.")
        return redirect(URL_HOME)

def registration_guardian_activate (request, guardian_activation_key):
    profile = UserProfile.get_UserProfile(guardian_activation_key=guardian_activation_key)
    if profile != None and profile.is_minor == True:
        profile.guardian_consented = True
        profile.save()

    #Send an email to the minor notifying that the guardian has approved!
    registration_profile = RegistrationProfile.objects.get(user=profile.user)
    email_subject = render_to_string(TEXTFILE_EMAIL_POST_GUARDIAN_ACTIVATION_SUBJECT, {})
    email_body = render_to_string(TEXTFILE_EMAIL_POST_GUARDIAN_ACTIVATION_BODY, {"activation_key": registration_profile.activation_key, "site": Site.objects.get_current() })
    send_email(email_subject, email_body, None, [profile.user.email])

    messages.success(request, "All done! Thank you for supporting your child in participating in EmergencyPetMatcher!")
    return redirect(URL_HOME)

def registration_activation_complete (request):
    messages.success (request, "Alright, you are all set registering! You may now login to EPM.")
    return redirect (URL_LOGIN)

def registration_register (request):
    if request.method == "GET": #Requesting the Registration Form Page
        return render_to_response (HTML_REGISTRATION_FORM, {
            'form':UserProfileForm(),
            "RECAPTCHA_CLIENT_SECRET": settings.RECAPTCHA_CLIENT_SECRET,
            "consent_form_minor_text":CONSENT_FORM_MINOR_TEXT,
            "consent_form_adult_text":CONSENT_FORM_ADULT_TEXT,
        }, RequestContext (request))

    elif request.method == "POST": #Submitting Registration Form Data
        if not request.POST.get("g-recaptcha-response"):
            messages.error(request, "Please fill in the RECAPTCHA.")
            return redirect(request.path)
        if not recaptcha_ok(request.POST.get("g-recaptcha-response")):
            messages.error(request, "RECAPTCHA was not correct. Please try again.")
            return redirect(request.path)

        form = UserProfileForm(request.POST, request.FILES)
        success, message = UserProfile.check_registration(post_obj=request.POST, userprofileform=form)

        if success == False:
            messages.error(request, message)
            return render_to_response(HTML_REGISTRATION_FORM, {
                "form": form,
                "RECAPTCHA_CLIENT_SECRET": settings.RECAPTCHA_CLIENT_SECRET,
                "consent_form_minor_text":CONSENT_FORM_MINOR_TEXT,
                "consent_form_adult_text":CONSENT_FORM_ADULT_TEXT,
            }, RequestContext (request))

        #Create a RegistrationProfile object, populate the potential User object, and be ready for activation.
        user = RegistrationProfile.objects.create_inactive_user(request.POST["username"], request.POST["email"], request.POST["password1"], Site.objects.get_current())

        #If this user truly is a minor, save some extra information to be checked during activation.
        if is_minor(request.POST.get("dob")) == True:
            user.userprofile.is_minor = True
            user.userprofile.guardian_email = request.POST.get("guardian_email")
            user.userprofile.guardian_activation_key = create_sha1_hash(user.username)
            #Send an email to the guardian with activation key.
            email_subject = render_to_string(TEXTFILE_EMAIL_GUARDIAN_SUBJECT, {})
            email_body = render_to_string(TEXTFILE_EMAIL_GUARDIAN_BODY, {
                "participant_email": request.POST["email"],
                "guardian_activation_key": user.userprofile.guardian_activation_key,
                "consent_form_guardian_text": CONSENT_FORM_GUARDIAN_TEXT,
                "site": Site.objects.get_current()
            })
            send_email(email_subject, email_body, None, [user.userprofile.guardian_email])

        user.userprofile.set_images(request.FILES.get("photo"), save=True, rotation=request.POST.get("img_rotation"))
        user.userprofile.dob = UserProfile.set_date_of_birth(request.POST.get("dob"))
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.save()
        print_info_msg ("RegistrationProfile now created for inactive user %s" % user)
        return redirect (URL_REGISTRATION_COMPLETE)
    else:
        raise Http404

def registration_complete (request):
    messages.success (request, "Thanks for registering for EPM. Look for an account verification email and click on the link to finish registering.")
    return redirect(URL_HOME)

def registration_disallowed (request):
    messages.error (request, "Sorry, we are not accepting registrations at this time. Please try again later.")
    return home(request)

def password_reset_complete (request):
    messages.success (request, "Great, your password has been changed. You can log in now.")
    return login_User(request)

def password_reset_done (request):
    messages.success (request, "We've e-mailed you instructions for setting your password to the e-mail address you submitted. You should be receiving it shortly.")
    return home(request)

def social_auth_get_details (request):
    print_info_msg("at home.views.social_auth_get_details")


def about (request):
    petreports = PetReport.objects.filter(closed = False).order_by("?")[:50]
    return render_to_response(HTML_ABOUT, {'petreports':petreports}, RequestContext(request))

def page_not_found(request):
    return render_to_response(HTML_404, {}, RequestContext(request))

def error(request):
    return render_to_response(HTML_500, {}, RequestContext(request))

def stats(request):
    return render_to_response(HTML_STATS, {
        "num_users": User.objects.count(),
        "num_petreports": PetReport.objects.count(),
        "num_lost_petreports": PetReport.objects.filter(status="Lost").count(),
        "num_found_petreports": PetReport.objects.filter(status="Found").count(),
        "num_petmatches": PetMatch.objects.count(),
        #Top 5 Users who have reported the most Pet Reports
        "top_5_reporters": UserProfile.objects.annotate(num_reports=Count("proposed_related")).order_by('-num_reports')[:5],
        #Top 5 Users who have matched the most pets
        "top_5_matchers": UserProfile.objects.annotate(num_matches=Count("proposed_by_related")).order_by('-num_matches')[:5],
        #Number of Upvotes
        "num_upvotes": PetMatch.objects.aggregate(Count("up_votes")),
        #Number of Downvotes
        "num_downvotes": PetMatch.objects.aggregate(Count("down_votes")),
        "num_petreunions": PetReunion.objects.count()
    }, RequestContext(request))
