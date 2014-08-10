from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout, login, authenticate 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import *
from django.contrib.sites.models import Site
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from social_auth import __version__ as version
from social_auth.views import auth
from social_auth.utils import setting
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.http import Http404
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
from django.utils import simplejson
from registration.models import RegistrationProfile
from registration.forms import RegistrationFormTermsOfService
from datetime import datetime
from social.models import UserProfile
from reporting.models import PetReport
from matching.models import PetMatch
from constants import *
from utilities.utils import *
from pprint import pprint
from utilities import logger
import oauth2 as oauth, random, urllib, hashlib, random, re, project.settings, registration

#Home view
def home (request):
    #Get the petreport and petmatch count for pagination purposes.
    petreport_count = len(PetReport.objects.filter(closed=False))
    petmatch_count = len(PetMatch.objects.filter(petcheck=None))
    successful_petmatch_count = len(PetMatch.objects.filter(is_successful=True))
    context =  {'petreport_count':petreport_count,
                'petmatch_count':petmatch_count,
                'successful_petmatch_count': successful_petmatch_count,
                'version': version}

    #Also get bookmark count for pagination purposes.
    if request.user.is_authenticated() == True:    
        up = request.user.get_profile()
        bookmark_count = len(up.bookmarks_related.all())
        context.update({ "bookmark_count": bookmark_count })

    return render_to_response(HTML_HOME, context, RequestContext(request))

def get_activities_json(request):
    if request.is_ajax() == True:
        activities = []

        #Let's populate the activity feed based upon whether the user is logged in.
        if request.user.is_authenticated() == True:
            print_info_msg ("get_activities_json(): Authenticated User - recent activities...")
            current_userprofile = request.user.get_profile()      
            activities += logger.get_activities_from_log(userprofile=current_userprofile, since_date=current_userprofile.last_logout, num_activities=ACTIVITY_FEED_LENGTH)            

        else:
            print_info_msg ("get_activities_json(): Anonymous User - random sample of activities...")
            # Get random activities for the anonymous user
            for userprof in UserProfile.objects.order_by("?").filter(user__is_active=True)[:ACTIVITY_FEED_LENGTH]:
                activities += logger.get_activities_from_log(userprofile=userprof, num_activities=1)

        #Zip it up in JSON and ship it out as an HTTP Response.
        json = simplejson.dumps ({"activities":activities})
        return HttpResponse(json, mimetype="application/json")     

    else:
        print_error_msg ("Request for get_activities_json not an AJAX request!")
        raise Http404           


#Given a PetReport ID, just return the PetReport JSON.
def get_PetReport(request, petreport_id):
    if (request.method == "GET") and (request.is_ajax() == True):
        petreport = get_object_or_404(PetReport, pk=petreport_id)
        json = simplejson.dumps ({"petreport":petreport.to_array()})
        pprint(petreport.to_array())
        return HttpResponse(json, mimetype="application/json")
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
        pet_reports = PetReport.get_PetReports_by_page(pet_reports, page)

        #Zip it up in JSON and ship it out as an HTTP Response.
        pet_reports = [{"ID": pr.id, 
                        "proposed_by_username": pr.proposed_by.user.username,
                        "pet_name": pr.pet_name, 
                        "pet_type": pr.pet_type, 
                        "img_path": pr.thumb_path.name } for pr in pet_reports]

        json = simplejson.dumps ({"pet_reports_list":pet_reports, "count":len(pet_reports), "total_count": petreport_count})
        return HttpResponse(json, mimetype="application/json")
    else:
        raise Http404        

#Given a PetMatch ID, just return the PetMatch JSON.
def get_PetMatch(request, petmatch_id):
    if (request.method == "GET") and (request.is_ajax() == True):
        petmatch = get_object_or_404(PetMatch, pk=petmatch_id)
        json = simplejson.dumps ({"petmatch":petmatch.toDICT()})
        return HttpResponse(json, mimetype="application/json")
    else:
        raise Http404  

def get_PetMatches(request, page=None):
    if request.is_ajax() == True:
        filtered_matches = PetMatch.objects.filter(is_successful=False).order_by("id").reverse()
        pet_matches = PetMatch.get_PetMatches_by_page(filtered_matches, page)

        #Get the petmatch count for pagination purposes.
        petmatch_count = len(filtered_matches)

        #Zip it up in JSON and ship it out as an HTTP Response.
        pet_matches = [{"ID": pm.id, 
                        "proposed_by_username": pm.proposed_by.user.username,
                        "lost_pet_name": pm.lost_pet.pet_name, 
                        "found_pet_name": pm.found_pet.pet_name, 
                        "lost_pet_img_path": pm.lost_pet.thumb_path.name,
                        "found_pet_img_path": pm.found_pet.thumb_path.name } for pm in pet_matches]

        json = simplejson.dumps ({"pet_matches_list":pet_matches, "count":len(pet_matches), "total_count": petmatch_count})
        return HttpResponse(json, mimetype="application/json")
    else:
        raise Http404

def get_successful_PetMatches(request, page=None):
    if request.is_ajax() == True:
        filtered_matches = PetMatch.objects.filter(is_successful=True).order_by("id").reverse()
        pet_matches = PetMatch.get_PetMatches_by_page(filtered_matches, page)

        #Get the petmatch count for pagination purposes.
        petmatch_count = len(filtered_matches)

        #Zip it up in JSON and ship it out as an HTTP Response.
        pet_matches = [{"ID": pm.id, 
                        "proposed_by_username": pm.proposed_by.user.username,
                        "lost_pet_name": pm.lost_pet.pet_name, 
                        "found_pet_name": pm.found_pet.pet_name, 
                        "lost_pet_img_path": pm.lost_pet.thumb_path.name,
                        "found_pet_img_path": pm.found_pet.thumb_path.name } for pm in pet_matches]

        json = simplejson.dumps ({"pet_matches_list":pet_matches, "count":len(pet_matches), "total_count": petmatch_count})
        return HttpResponse(json, mimetype="application/json")
    else:
        raise Http404

@login_required
def get_bookmarks(request, page=None):
    if request.is_ajax() == True:
        up = request.user.get_profile()
        bookmarks = up.bookmarks_related.all()

        #Get the bookmark count for pagination purposes.
        bookmarks_count = len(bookmarks)

        #Now get just a page of bookmarks if page # is available.
        bookmarks = PetReport.get_bookmarks_by_page(bookmarks, page)

        #Zip it up in JSON and ship it out as an HTTP Response.
        bookmarks = [{"ID": pr.id, 
                        "proposed_by_username": pr.proposed_by.user.username,
                        "pet_name": pr.pet_name, 
                        "pet_type": pr.pet_type, 
                        "img_path": pr.thumb_path.name } for pr in bookmarks]

        json = simplejson.dumps ({"bookmarks_list":bookmarks, "count":len(bookmarks), "total_count": bookmarks_count})
        return HttpResponse(json, mimetype="application/json")
    else:
        raise Http404        


def login_User(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user != None:
            if user.is_active == True:
                userprofile = user.get_profile()

                #if log_exists(userprofile) == False:
                 #   logger.log_activity(ACTIVITY_ACCOUNT_CREATED, userprofile)

                login(request, user)
                messages.success(request, 'Welcome, %s!' % (username))
                logger.log_activity(ACTIVITY_LOGIN, user.get_profile())
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
    print_info_msg ("logger out UserProfile {%s}" % request.user.get_profile())

    # Update to last_logout date field
    user = get_object_or_404(UserProfile, pk=request.user.get_profile().id)
    user.last_logout = datetime.now()
    user.save()
 
    logger.log_activity(ACTIVITY_LOGOUT, request.user.get_profile())
    messages.success(request, "You have successfully logged out.")
    logout(request)
    return redirect(URL_HOME)

def registration_activate (request, activation_key=None, backend=None):
    print_info_msg ("Activation Key: %s" % activation_key)

    #Does the activation key exist within a RegistrationProfile? 
    #(i.e. is somebody actually trying to activate an account or resurrect an old activation link?)
    try:
        rp = RegistrationProfile.objects.get(activation_key=activation_key)
        profile = rp.user.get_profile()

    except RegistrationProfile.DoesNotExist:
        messages.error(request, "This account has already been activated!")
        return redirect(URL_HOME)

    #Need to check if user is a minor and if parent/guardian consented.
    pprint(profile.__dict__)
    if profile.is_minor == False or profile.guardian_consented == True:
        activated_user = RegistrationProfile.objects.activate_user(activation_key)
        print_info_msg ("RegistrationProfile now activated for active user %s" % activated_user)
        return redirect (URL_ACTIVATION_COMPLETE)
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

def disp_TC(request):
    # request.session['agreed'] = False
    return render_to_response(HTML_TC, {}, RequestContext(request))

def disp_TC_18(request):
    # request.session['agreed'] = False
    return render_to_response(HTML_TC_18, {}, RequestContext(request))

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
        success, message = UserProfile.check_registration(form, request.POST)

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

        #If this user truly is a minor, save some extra information to be checked during activation.
        if is_minor(request.POST["date_of_birth"]) == True:
            profile = user.get_profile()
            profile.is_minor = True
            profile.guardian_email = request.POST.get("guardian_email")
            profile.guardian_activation_key = create_sha1_hash(user.username)
            profile.save()

            #Send an email to the guardian with activation key.
            email_body = render_to_string(TEXTFILE_EMAIL_GUARDIAN_BODY, 
                {   "participant_email": request.POST["email"], 
                    "guardian_activation_key": profile.guardian_activation_key,
                    "site": Site.objects.get_current() })
            email_subject = render_to_string(TEXTFILE_EMAIL_GUARDIAN_SUBJECT, {})
            send_mail(email_subject, email_body, None, [profile.guardian_email])                        

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
    name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
    details = request.session[name]['kwargs']['details']
    backend = request.session[name]['backend']
    link = None
    print_debug_msg(details)
    
    #We have retrieved a picture link from Facebook OR from Twitter, otherwise raise Http404.
    if backend =='facebook':
        # profile pic
        pic_url = "http://graph.facebook.com/%s/picture?type=large" % request.session[name]['kwargs']['response']['id']
        # personal webpage
        link = request.session[name]['kwargs']['response']['link']
    elif backend == 'twitter':
        pic_url = request.session[name]['kwargs']['response'].get('profile_image_url', '').replace('_normal', '')
    else:
        raise Http404

    #If the first-time user submits the form...
    if request.method == 'POST':
        form = RegistrationFormTermsOfService(request.POST)
        success, message = UserProfile.check_registration(form)

        if success == False:
            messages.error(request, message)
            return render_to_response(HTML_SOCIAL_AUTH_FORM,{   'username':details['username'],
                                                                'first_name':details['first_name'], 
                                                                'last_name':details['last_name'], 
                                                                'email':details['email'], 
                                                                'pic_url':pic_url, 
                                                                "tos_minor_text":TOS_MINOR_TEXT,
                                                                "tos_adult_text":TOS_ADULT_TEXT,
                                                                'link':link
                                                            }, RequestContext(request))            


        #Create a RegistrationProfile object, populate the potential User object, and be ready for activation.
        user = RegistrationProfile.objects.create_inactive_user(request.POST["username"], 
                                                                request.POST["email"], 
                                                                request.POST["password1"], 
                                                                Site.objects.get_current())

        #If this user truly is a minor, save some extra information to be checked during activation.
        if is_minor(request.POST["date_of_birth"]) == True:
            profile = user.get_profile()
            profile.is_minor = True
            profile.guardian_email = request.POST.get("guardian_email")
            profile.guardian_activation_key = create_sha1_hash(user.username)
            profile.save()

            #Send an email to the guardian with activation key.
            email_body = render_to_string(TEXTFILE_EMAIL_GUARDIAN_BODY, 
                {   "participant_email": request.POST["email"], 
                    "guardian_activation_key": profile.guardian_activation_key,
                    "site": Site.objects.get_current() })
            email_subject = render_to_string(TEXTFILE_EMAIL_GUARDIAN_SUBJECT, {})
            send_mail(email_subject, email_body, None, [profile.guardian_email])   

        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")

        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.save()
        print_info_msg ("(SOCIAL AUTH): RegistrationProfile now created for inactive user %s" % user)
        user_dict = {"username":username, "email":email, "first_name":first_name, "last_name":last_name}
        request.session["user_dict"] = user_dict
        return redirect(URL_SOCIAL_AUTH_COMPLETE + backend, backend=backend)

    # If the user has logged in for the first time as facebook or twitter user, get details.
    else:
        return render_to_response(HTML_SOCIAL_AUTH_FORM, {  'username':details['username'],
                                                            'first_name':details['first_name'], 
                                                            'last_name':details['last_name'], 
                                                            'email':details['email'], 
                                                            'pic_url':pic_url, 
                                                            "tos_minor_text":TOS_MINOR_TEXT,
                                                            "tos_adult_text":TOS_ADULT_TEXT,
                                                            'link':link}, RequestContext(request))


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
