from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout, login, authenticate 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import *
from django.contrib.sites.models import Site
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.http import Http404
from urllib import urlopen
from StringIO import StringIO
from django.core import mail
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.timezone import now as datetime_now
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.contrib import messages
from registration.models import RegistrationProfile
from registration.forms import RegistrationFormTermsOfService
from datetime import datetime
from models import Activity
from socializing.models import UserProfile
from reporting.models import PetReport
from matching.models import PetMatch
from constants import *
from reporting.constants import NUM_PETREPORTS_HOMEPAGE, NUM_BOOKMARKS_HOMEPAGE
from matching.constants import NUM_PETMATCHES_HOMEPAGE
from utilities.utils import *
from pprint import pprint
import oauth2 as oauth, json, random, urllib, hashlib, random, re, project.settings, registration

#Home view
def home (request):
    #Get the petreport and petmatch count for pagination purposes.
    petreport_count = len(PetReport.objects.filter(closed=False))
    petmatch_count = len(PetMatch.objects.filter(petcheck=None))
    successful_petmatch_count = len(PetMatch.objects.filter(is_successful=True))
    context =  {'petreport_count':petreport_count,
                'petmatch_count':petmatch_count,
                'successful_petmatch_count': successful_petmatch_count}

    #Also get bookmark count for pagination purposes.
    if request.user.is_authenticated() == True:    
        up = request.user.userprofile
        bookmark_count = len(up.bookmarks_related.all())
        context.update({ "bookmark_count": bookmark_count })

    return render_to_response(HTML_HOME, context, RequestContext(request))

def get_activities(request, page=None):
    if request.is_ajax() == True:

        #Let's populate the activity feed based upon whether the user is logged in.
        if request.user.is_authenticated() == True:
            print_info_msg ("get_activities(): Authenticated User - recent activities...")
            current_userprofile = request.user.userprofile      
            # activities = Activity.get_activities_for_feed(page=page, since_date=current_userprofile.last_logout, userprofile=current_userprofile)            
            activities = Activity.get_Activities_for_feed(page=page, since_date=None, userprofile=None)
        else:
            activities = Activity.get_Activities_for_feed(page=page, since_date=None, userprofile=None)

        #Zip it up in JSON and ship it out as an HTTP Response.
        activities = [{ "activity"          : activity.activity,
                        "date_posted"       : activity.date_posted.ctime(),
                        "profile"           : activity.userprofile.to_DICT(),
                        "source"            : activity.get_source_DICT(),
                        "text"              : activity.text } for activity in activities]

        payload = json.dumps ({"activities":activities})
        return HttpResponse(payload, mimetype="application/json")     

    else:
        print_error_msg ("Request for get_activities not an AJAX request!")
        raise Http404           


#Given a PetReport ID, just return the PetReport JSON.
def get_PetReport(request, petreport_id):
    if (request.method == "GET") and (request.is_ajax() == True):
        petreport = get_object_or_404(PetReport, pk=petreport_id)
        payload = json.dumps ({"petreport":petreport.to_array()})
        return HttpResponse(payload, mimetype="application/json")
    else:
        raise Http404        

#Given a Page Number, return a list of PetReports.
def get_PetReports(request, page=None):
    if request.is_ajax() == True:
        #Grab all Pets.
        pet_reports = PetReport.objects.filter(closed = False).order_by("id").reverse()
        #Get the petreport count for pagination purposes.
        petreport_count = len(pet_reports)
        #Now get just a page of PetReports if page # is available.
        pet_reports = get_objects_by_page(pet_reports, page, limit=NUM_PETREPORTS_HOMEPAGE)
        #Zip it up in JSON and ship it out as an HTTP Response.
        pet_reports = [{"ID"                    : pr.id, 
                        "proposed_by_username"  : pr.proposed_by.user.username,
                        "pet_name"              : pr.pet_name, 
                        "pet_type"              : pr.pet_type, 
                        "img_path"              : pr.thumb_path.name } for pr in pet_reports]

        payload = json.dumps ({"pet_reports_list":pet_reports, "count":len(pet_reports), "total_count": petreport_count})
        return HttpResponse(payload, mimetype="application/json")
    else:
        raise Http404     

@login_required
def get_bookmarks(request, page=None):
    if request.is_ajax() == True:
        up = request.user.userprofile
        bookmarks = up.bookmarks_related.all()
        #Get the bookmark count for pagination purposes.
        bookmarks_count = len(bookmarks)
        #Now get just a page of bookmarks if page # is available.
        bookmarks = get_objects_by_page(bookmarks, page, limit=NUM_BOOKMARKS_HOMEPAGE)
        #Zip it up in JSON and ship it out as an HTTP Response.
        bookmarks = [{  "ID"                    : pr.id, 
                        "proposed_by_username"  : pr.proposed_by.user.username,
                        "pet_name"              : pr.pet_name, 
                        "pet_type"              : pr.pet_type, 
                        "img_path"              : pr.thumb_path.name } for pr in bookmarks]

        bookmarks = json.dumps ({"bookmarks_list":bookmarks, "count":len(bookmarks), "total_count": bookmarks_count})
        return HttpResponse(bookmarks, mimetype="application/json")
    else:
        raise Http404        


#Given a PetMatch ID, just return the PetMatch JSON.
def get_PetMatch(request, petmatch_id):
    if (request.method == "GET") and (request.is_ajax() == True):
        petmatch = get_object_or_404(PetMatch, pk=petmatch_id)
        payload = json.dumps ({"petmatch":petmatch.to_DICT()})
        return HttpResponse(payload, mimetype="application/json")
    else:
        raise Http404  

def get_PetMatches(request, successful=None, page=None):
    if request.is_ajax() == True:
        successful = bool(int(successful or 0))
        print_info_msg("SUCCESSFUL:%s" % successful)
        filtered_matches = PetMatch.objects.filter(is_successful=successful, has_failed=False).order_by("id").reverse()
        pet_matches = get_objects_by_page(filtered_matches, page, limit=NUM_PETMATCHES_HOMEPAGE)

        #Get the petmatch count for pagination purposes.
        petmatch_count = len(filtered_matches)
        #Zip it up in JSON and ship it out as an HTTP Response.
        pet_matches = [{"ID"                    : pm.id, 
                        "proposed_by_username"  : pm.proposed_by.user.username,
                        "lost_pet_name"         : pm.lost_pet.pet_name, 
                        "found_pet_name"        : pm.found_pet.pet_name, 
                        "lost_pet_img_path"     : pm.lost_pet.thumb_path.name,
                        "found_pet_img_path"    : pm.found_pet.thumb_path.name } for pm in pet_matches]

        payload = json.dumps ({"pet_matches_list":pet_matches, "count":len(pet_matches), "total_count": petmatch_count})
        return HttpResponse(payload, mimetype="application/json")
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
                next_url = request.REQUEST ['next']

                if "//" in next_url and re.match(r'[^\?]*//', next_url):
                    next_url = settings.LOGIN_REDIRECT_URL
                return redirect(next_url)

            else:
                messages.error(request, "You haven't activated your account yet. Please check your email.")
        else:
            messages.error(request, 'Invalid Login credentials. Please try again.')

    try: 
        next = request.REQUEST ['next']
    except KeyError: #This only happens if the user tries to plug in the login URL without a 'next' parameter...
        next = URL_HOME

    form = AuthenticationForm()
    return render_to_response(HTML_LOGIN, {'form':form}, RequestContext(request, {'next': next}))


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

    messages.success(request, "All done! Thank you for supporting your child in participating in EmergencyPetMatcher!")
    return redirect(URL_HOME)

def registration_activation_complete (request):
    messages.success (request, "Alright, you are all set registering! You may now login to EPM.")
    return redirect (URL_LOGIN)     

def registration_register (request):
    #Requesting the Registration Form Page
    if request.method == "GET":
        return render_to_response (HTML_REGISTRATION_FORM, 
            {   "form":RegistrationFormTermsOfService(),
                "tos_minor_text":TOS_MINOR_TEXT,
                "tos_adult_text":TOS_ADULT_TEXT,
            }, RequestContext (request))

    #Submitting Registration Form Data
    elif request.method == "POST":
        form = RegistrationFormTermsOfService(request.POST)
        pprint(request.POST)
        success, message = UserProfile.check_registration(post_obj=request.POST, registration_form=form)
        print_debug_msg(message)

        if success == False:
            messages.error(request, message)
            return render_to_response(HTML_REGISTRATION_FORM, 
                {   "form": form,
                    "tos_minor_text":TOS_MINOR_TEXT,
                    "tos_adult_text":TOS_ADULT_TEXT
                }, RequestContext (request))
        
        #Create a RegistrationProfile object, populate the potential User object, and be ready for activation.
        user = RegistrationProfile.objects.create_inactive_user(request.POST["username"], 
                                                                request.POST["email"], 
                                                                request.POST["password1"], 
                                                                Site.objects.get_current())
        
        #Grab the UserProfile object.
        profile = user.userprofile

        #If this user truly is a minor, save some extra information to be checked during activation.
        if is_minor(request.POST["date_of_birth"]) == True:
            profile.is_minor = True
            profile.guardian_email = request.POST.get("guardian_email")
            profile.guardian_activation_key = create_sha1_hash(user.username)
            profile.save()

            #Send an email to the guardian with activation key.
            email_subject = render_to_string(TEXTFILE_EMAIL_GUARDIAN_SUBJECT, {})
            email_body = render_to_string(TEXTFILE_EMAIL_GUARDIAN_BODY, {   "participant_email": request.POST["email"],
                                                                            "guardian_activation_key": profile.guardian_activation_key,
                                                                            "site": Site.objects.get_current() })
            
            send_mail(email_subject, email_body, None, [profile.guardian_email])

        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")

        #Format the Date of Birth and store it.
        profile.set_date_of_birth(request.POST.get("date_of_birth"))
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
   

'''
def social_auth_login(request, backend):
    """
        This view is a wrapper to social_auths auth
        It is required, because social_auth just throws ValueError and gets user to 500 error
        after every unexpected action. This view handles exceptions in human friendly way.
        See https://convore.com/django-social-auth/best-way-to-handle-exceptions/
    """
    """
    Q: How can I add messages.success(request, 'Welcome, %s!' % (username)) in ths function?
    """
    print_info_msg("At home.views.social_auth_login()")
    try:
        # if everything is ok, then original view gets returned, no problem
         return auth(request, backend)
    except IntegrityError, error:
        return render_to_response(HTML_SOCIAL_AUTH_FORM, locals(), RequestContext(request))


def social_auth_disallowed (request):
    messages.error (request, "Sorry, we can not accept your social registration. Please try again later.")
    return home(request)


'''


def about (request):
    petreports = PetReport.objects.filter(closed = False).order_by("?")[:50]
    return render_to_response(HTML_ABOUT, {'petreports':petreports}, RequestContext(request))



class RemoteUserMiddleware(object):
    def process_response(self, request, response):
        if hasattr(request, 'user'):
            if request.user.is_authenticated():
                response['X-Remote-User-Name'] = request.user.username
                response['X-Remote-User-Id'] = request.user.id
        return response
