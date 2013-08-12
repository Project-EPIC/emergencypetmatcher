from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout, login, authenticate 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import *
from django.contrib.sites.models import Site
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from social_auth import __version__ as version
from social_auth.utils import setting
from social_auth.views import auth
from django.core.mail import EmailMessage
from django.db import IntegrityError
from django.http import Http404
from django.core import mail
from django.core.validators import email_re
from django.core.urlresolvers import reverse
from django.forms.models import model_to_dict
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.timezone import now as datetime_now
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import simplejson
from registration.models import RegistrationProfile
from registration.forms import RegistrationForm
from datetime import datetime
from utils import *
from home.models import *
from constants import *
from pprint import pprint
import oauth2 as oauth, logger, random, urllib, hashlib, random, re, project.settings, registration

#Home view
def home (request):
    #Get the petreport and petmatch count for pagination purposes.
    petreport_count = len(PetReport.objects.filter(closed=False))
    petmatch_count = len(PetMatch.objects.filter(is_open=True))

    if request.user.is_authenticated() == True:
        #Also get bookmark count for pagination purposes.
        up = request.user.get_profile()
        bookmark_count = len(up.bookmarks_related.all())
        return render_to_response(HTML_HOME, {  'petreport_count':petreport_count, 
                                                'petmatch_count':petmatch_count,
                                                'bookmark_count':bookmark_count,
                                                'last_login': request.session.get('social_auth_last_login_backend'), 
                                                'version':version}, 
                                                RequestContext(request))
    else:
        return render_to_response(HTML_HOME, {  'petreport_count':petreport_count,
                                                'petmatch_count':petmatch_count,
                                                'version': version}, 
                                                RequestContext(request))

def get_activities_json(request):
    #Let's populate the activity feed based upon whether the user is logged in.
    if request.is_ajax() == True:
        # Initialize the activity list
        activities = []

        if request.user.is_authenticated() == True:
            print_info_msg ("get_activities_json(): Authenticated User - recent activities...")
            current_userprofile = request.user.get_profile()      

            # Get all activities that are associated with the UserProfiles I follow
            print_info_msg ("Fetching activities related to userprofiles I follow...")
            for following in current_userprofile.following.all().order_by("?")[:ACTIVITY_FEED_LENGTH]:
                activities += logger.get_recent_activities_from_log(userprofile=following, current_userprofile=current_userprofile,
                    since_date=current_userprofile.last_logout) 

            # Get all activities from (my) UserProfile's log file that show who has followed (me).
            print_info_msg ("Fetching activities related to userprofiles who have followed me...")
            activities += logger.get_recent_activities_from_log(userprofile=current_userprofile, current_userprofile=current_userprofile, 
                 since_date=current_userprofile.last_logout, activity=ACTIVITY_FOLLOWER)
        
            # Get all activities that are associated to the PetReports (I) bookmarked
            print_info_msg ("Fetching activities related to bookmarks...")
            activities += logger.get_bookmark_activities(userprofile=current_userprofile, since_date=current_userprofile.last_logout)

        else:
            print_info_msg ("get_activities_json(): Anonymous User - random sample of activities...")
            # Get random activities for the anonymous user           
            for userprof in UserProfile.objects.order_by("?").filter(user__is_active=True)[:ACTIVITY_FEED_LENGTH]:
                activities += logger.get_recent_activities_from_log(userprofile=userprof, current_userprofile=None, num_activities=1)


        # Sort the activity feed list according the log date
        activities.sort() 

        # Remove log date info and include only feed text 
        temp_activities = []
        activities_length = len(activities)

        for x in range(0, activities_length):
            activities [x] = activities[x][1]

        #ERROR message print to flag for potential problem in the log directory.
        #if request.user.is_authenticated() == False and activities_length != ACTIVITY_FEED_LENGTH:
         #   print_error_msg ("Length of activity list is %d when it should be ACTIVITY_FEED_LENGTH = %d" % (activities_length, ACTIVITY_FEED_LENGTH))

        #Zip it up in JSON and ship it out as an HTTP Response.
        json = simplejson.dumps ({"activities":activities})
        pprint(activities)
        return HttpResponse(json, mimetype="application/json")     

    else:
        print_error_msg ("Request for get_activities_json not an AJAX request!")
        raise Http404           


#Given a PetReport ID, just return the PetReport JSON.
def get_PetReport(request, petreport_id):
    if (request.method == "GET") and (request.is_ajax() == True):
        petreport = get_object_or_404(PetReport, pk=petreport_id)
        json = simplejson.dumps ({"petreport":petreport.toDICT()})
        return HttpResponse(json, mimetype="application/json")
    else:
        raise Http404        

#Given a Page Number, return a list of PetReports.
def get_PetReports(request, page=None):
    if request.is_ajax() == True:
        #Grab all Pets.
        pet_reports = PetReport.objects.filter(closed = False).order_by("id").reverse()

        #Now get just a page of PetReports if page # is available.
        pet_reports = PetReport.get_PetReports_by_page(pet_reports, page)

        #Get the petreport count for pagination purposes.
        petreport_count = len(PetReport.objects.filter(closed=False))

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

        #Check if there's a specified page number.
        if (page != None and page > 0):
            page = int(page)
            pet_matches = PetMatch.objects.filter(is_open = True).order_by("id").reverse()[((page-1) * NUM_PETMATCHES_HOMEPAGE):((page-1) * NUM_PETMATCHES_HOMEPAGE + NUM_PETMATCHES_HOMEPAGE)]
        else:
            #Get Pet Match objects and send them off as JSON.
            pet_matches = PetMatch.objects.filter(is_open = True).order_by("id").reverse()

        #Get the petmatch count for pagination purposes.
        petmatch_count = len(PetMatch.objects.filter(is_open=True))

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

        #Check if there's a specified page number.
        if (page != None and page > 0):
            page = int(page)
            bookmarks = up.bookmarks_related.all()[((page-1) * NUM_BOOKMARKS_HOMEPAGE):((page-1) * NUM_BOOKMARKS_HOMEPAGE + NUM_BOOKMARKS_HOMEPAGE)]

        else:
            #Get Pet Match objects and send them off as JSON.
            bookmarks = up.bookmarks_related.all()

        #Get the petreport count for pagination purposes.
        bookmarks_count = len(up.bookmarks_related.all())

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
    u = get_object_or_404(UserProfile, pk=request.user.get_profile().id)
    u.last_logout = datetime.datetime.now()
    u.save()
 
    logger.log_activity(ACTIVITY_LOGOUT, request.user.get_profile())
    messages.success(request, "You have successfully logged out.")
    logout(request)
    return redirect(URL_HOME)

def registration_activate (request, activation_key=None, backend=None):
    print_info_msg ("Activation Key: %s" % activation_key)

    #Does the activation key exist within a RegistrationProfile? (i.e. is somebody actually trying to activate an account or resurrect an old activation link?)
    try:
        rp = RegistrationProfile.objects.get(activation_key=activation_key)

    except RegistrationProfile.DoesNotExist:
        messages.error(request, "This account has already been activated!")
        return redirect(URL_HOME)

    #Specify the django-registration default backend for activating this account. 
    activated_user = RegistrationProfile.objects.activate_user(activation_key)
    print_info_msg ("RegistrationProfile now activated for active user %s" % activated_user)
    return redirect (URL_ACTIVATION_COMPLETE)

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
        return render_to_response (HTML_REGISTRATION_FORM, {"form":RegistrationForm()}, RequestContext (request))

    #Submitting Regisration Form Data
    elif request.method == "POST":
        #Need to check if data is OK for continuing registration.        
        form = RegistrationForm(request.POST)
        email = request.POST ["email"]
        username = request.POST ["username"]
        password = password1 = request.POST ["password1"]
        password2 = request.POST ["password2"]

        if password1 != password2:
            print_info_msg("Passwords do not match. Registration failed for user.")
            messages.error(request, "Passwords do not match. Please try again.")
            return redirect (URL_REGISTRATION)

        #Does the input username exist already in another user?
        if User.objects.filter(username=username).exists() == True:
            print_info_msg("Existing Username - Registration failed for user.")
            messages.error(request, "The username you provided already exists. Try another username.")
            return redirect (URL_REGISTRATION)

        #Does the input email exist already in another user?
        if User.objects.filter(email=email).exists() == True:
            print_info_msg("Existing Email - Registration failed for user.")
            messages.error(request, "The email address you provided already exists. Try another email.")
            return redirect (URL_REGISTRATION)

        #Did this user (or any other user) already try to register before with this username?
        if RegistrationProfile.objects.filter(user__username=username).exists() == True:
            print_info_msg("Existing Username in Registration - Registration failed for user.")
            messages.error(request, "The username you provided already exists. Try another email.")
            return redirect (URL_REGISTRATION)

        #Did this user (or any other user) already try to register before with this email?
        if RegistrationProfile.objects.filter(user__email=email).exists() == True:
            print_info_msg("Existing Email - Registration failed for user.")
            messages.error(request, "The email address you provided already exists. Try another email.")
            return redirect (URL_REGISTRATION)

        #else, create the new inactive users here.
        new_user = RegistrationProfile.objects.create_inactive_user(username, email, password, Site.objects.get_current())
        print_info_msg ("RegistrationProfile now created for inactive user %s" % new_user)

        #Redirect back to Home
        return redirect (URL_REGISTRATION_COMPLETE)

    else:
        raise Http404

def registration_complete (request):
    messages.success (request, "Thanks for registering for EPM. Look for an account verification email and click on the link to finish registering.")
    return redirect(URL_HOME)

def registration_disallowed (request):
    messages.error (request, "Sorry, we are not accepting registrations at this time. Please try again later.")
    return home(request)

def social_auth_disallowed (request):
    messages.error (request, "Sorry, we can not accept your social registration. Please try again later.")
    return home(request)

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
    try:
        # if everything is ok, then original view gets returned, no problem
         return auth(request, backend)
    except IntegrityError, error:
        return render_to_response(HTML_SOCIAL_AUTH_FORM, locals(), RequestContext(request))


#Used by social auth pipeline to get a username value when authenticate a social user for the first time
def get_social_details(request):
    name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
    detail = request.session[name]['kwargs']['details']
    link = ""
    print request.session[name]['kwargs']

    if request.session[name]['backend'] =='facebook':
        # profile pic
        pic_url = "http://graph.facebook.com/%s/picture?type=large" % request.session[name]['kwargs']['response']['id']
        # personal webpage
        link = request.session[name]['kwargs']['response']['link']
        # print link
    elif request.session[name]['backend'] == 'twitter':
        pic_url = request.session[name]['kwargs']['response'].get('profile_image_url', '').replace('_normal', '')
    else:
        pass

    username_accepted = False
    email_accepted = False
    message = []

    if request.method == 'POST':
        if request.POST.get('username'):
            request.session['saved_username'] = request.POST['username']
            backend = request.session[name]['backend']

            try:
                # Check for a duplicate username
                existing_user = User.objects.get(username=request.POST.get('username'))
                message.append("Sorry! '%s' already exists. Please try another one." % request.POST.get('username'))
            except:
                username_accepted = True

        else:
            messages.error(request, "Username field is required.")

        if request.POST.get('email'):
            request.session[name]['kwargs']['details']['email'] = request.POST['email']
            backend = request.session[name]['backend']

            try:
                # Check for a duplicate email
                existing_email = User.objects.get(email=request.POST.get('email'))
                message.append("Sorry! '%s' already exists. Please try another one." % request.POST.get('email'))
            except:
                email_accepted = True

        else:
            message.error(request, "Email field is required.")

        request.session[name]['kwargs']['details']['first_name'] = request.POST['first_name']
        request.session[name]['kwargs']['details']['last_name'] = request.POST['last_name']

        if username_accepted and email_accepted:
            messages.success(request, 'Welcome, %s!' % (request.POST.get('username')))
            return redirect(URL_SOCIAL_AUTH_COMPLETE, backend=backend)

        else:
            return render_to_response(HTML_SOCIAL_AUTH_FORM, {'username':request.POST['username'], 'first_name':request.POST['first_name'], 'last_name':request.POST['last_name'], 'email':request.POST['email'], 'pic_url':pic_url, 'link':link}, RequestContext(request))

    else:
        # If the user has logged in for the first time as facebook or twitter user
        # Get details from the associated social account
        return render_to_response(HTML_SOCIAL_AUTH_FORM, {'username':detail['username'], 'first_name':detail['first_name'], 'last_name':detail['last_name'], 'email':detail['email'], 'pic_url':pic_url, 'link':link}, RequestContext(request))



@login_required
def get_UserProfile_page(request, userprofile_id):   
    u = get_object_or_404(UserProfile, pk=userprofile_id)
    #Grab Proposed PetReports.
    proposed_petreports = u.proposed_related.all()
    #Grab Proposed PetMatches.
    proposed_petmatches = u.proposed_by_related.all()
    #Grab the following list.
    following_list = u.following.all()
    #Grab the followers list.
    followers_list = u.followers.all()
    return render_to_response(HTML_USERPROFILE,{    "show_profile":u,
                                                    "proposed_petreports": proposed_petreports, 
                                                    "proposed_petmatches":proposed_petmatches,
                                                    "following_list": following_list,
                                                    "followers_list": followers_list}, RequestContext(request))

@login_required
def follow_UserProfile(request): 
    if request.method == "POST":
        userprofile = request.user.userprofile
        target_userprofile_id = request.POST["target_userprofile_id"]
        target_userprofile = get_object_or_404(UserProfile, pk=target_userprofile_id)

        #If the userprofile IDs do not match...
        if userprofile.id != target_userprofile.id:
            #Has this UserProfile already followed this target UserProfile?
            if target_userprofile in userprofile.following.all():
                messages.error(request, "You are already following " + str(target_userprofile.user.username) + ".")

            else:
                userprofile.following.add(target_userprofile)
                # add points to the user who is being followed (i.e. the target_userprofile) 
                target_userprofile.update_reputation(ACTIVITY_USER_BEING_FOLLOWED)
                messages.success(request, "You are now following " + str(target_userprofile.user.username) + ".")     

                # Log the following activity for this UserProfile
                logger.log_activity(ACTIVITY_FOLLOWING, userprofile, target_userprofile)

            return redirect (URL_USERPROFILE + str(target_userprofile.id))

    else:
        raise Http404

@login_required
def unfollow_UserProfile(request): 
    if request.method == "POST":
        userprofile = request.user.userprofile
        target_userprofile_id = request.POST["target_userprofile_id"]
        target_userprofile = get_object_or_404(UserProfile, pk=target_userprofile_id)

        #If the userprofile IDs do not match...
        if userprofile.id != target_userprofile.id:

            #If this UserProfile is actually following the target UserProfile...
            if target_userprofile in userprofile.following.all():
                userprofile.following.remove(target_userprofile)
                # remove points to the use who has been unfollowed (i.e. the target_userprofile)
                target_userprofile.update_reputation(ACTIVITY_USER_BEING_UNFOLLOWED)
                messages.success(request, "You are no longer following " + str(target_userprofile.user.username) + ".") 
                # Log the unfollowing activity for this UserProfile
                logger.log_activity(ACTIVITY_UNFOLLOWING, userprofile, target_userprofile)
                return redirect(URL_USERPROFILE + str(target_userprofile.id))

            else:
                raise Http404
        else:
            raise Http404
    else:
        raise Http404

@login_required
def message_UserProfile(request):
    if request.method == "POST":
        #Collect Text of Message
        message = request.POST ["message"]
        target_userprofile_id = request.POST ["target_userprofile_id"]
        target_userprofile = get_object_or_404(UserProfile, pk=target_userprofile_id)
        from_userprofile = request.user.get_profile()

        #You cannot send a message to yourself!
        if from_userprofile.id == target_userprofile.id:
            messages.error (request, "You cannot send a message to yourself.")
            return redirect(URL_USERPROFILE + str(from_userprofile.id))

        print_info_msg ("Sending an email message from %s to %s" % (from_userprofile.user.username, target_userprofile.user.username))

        #Send message to UserProfile
        completed = from_userprofile.send_email_message_to_UserProfile(target_userprofile, message, test_email=False)

        if completed == True:
            messages.success(request, "You have successfully sent your message to %s" % target_userprofile.user.username + ".") 
        else:
            messages.error(request, "Sorry, your message could not be sent because this user's email address is invalid.")

        return redirect(URL_USERPROFILE + str(target_userprofile_id))
    

@login_required
def editUserProfile_page(request):
    if request.method=='GET':
        user = request.user
        form = UserProfileForm(initial={'first_name': user.first_name,'last_name': user.last_name,'username':user.username,'email':user.email})
        update_User_info_form = []
        update_User_pwd_form = []
        photo = str(user.get_profile().img_path)

        for field in form:
            if 'password' in field.name:
                update_User_pwd_form.append(field)
            else:
                update_User_info_form.append(field)

        # 'update_User_pwd_form' shouldn't be shown to social_auth users because they can't change their passwords.
        if user.social_auth.count() == 0:
            return render_to_response(HTML_EDITUSERPROFILE_FORM, {"update_User_info_form": update_User_info_form, "update_User_pwd_form": update_User_pwd_form, "profile_picture":photo}, RequestContext(request))
        else:
            return render_to_response(HTML_EDITUSERPROFILE_FORM, {"update_User_info_form": update_User_info_form, "profile_picture":photo}, RequestContext(request))
    else:
        raise Http404


@login_required
def update_User_info(request):
    if request.method == "POST":
        user = request.user
        user_changed = False
        email_changed = False
        userprofile_form = UserProfileForm(request.POST, request.FILES)

        #Check if the form is valid.
        if userprofile_form.is_valid() == True:
            pprint(request.POST)
            pprint (request.FILES)

            #Change the photo 
            if "photo" in request.FILES:
                user_changed = True
                photo = request.FILES ["photo"]
                pprint(photo.__dict__)
                user.userprofile.set_images(photo)

            #Check if username has changed.
            if request.POST ["username"] != user.username:
                try:
                    #Does a UserProfile with the input username exist already?
                    existing_userprofile = UserProfile.objects.get(user__username=request.POST["username"])

                    if existing_userprofile != None:
                        messages.error(request, "Sorry, that username is already being used. Try another one.")
                        return redirect(URL_EDITUSERPROFILE)

                except UserProfile.DoesNotExist:
                    user.username = request.POST ["username"]
                    user_changed = True

            #Check if email has changed.
            if request.POST["email"] != user.email:

                if email_re.match(request.POST["email"]):
                    subject = render_to_string(TEXTFILE_EMAIL_ACTIVATION_SUBJECT)
                    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
                    activation_key = hashlib.sha1(salt + user.username).hexdigest()
                    print_info_msg ('user: %s \tactivation-key: %s' % (user, activation_key))

                    try:
                        edit_userprofile = EditUserProfile.objects.get(user=user)
                        edit_userprofile.activation_key = activation_key

                    except EditUserProfile.DoesNotExist:
                        edit_userprofile = EditUserProfile.objects.create(user=user, activation_key = activation_key)

                    edit_userprofile.new_email = request.POST ["email"]
                    edit_userprofile.date_of_change = datetime_now()
                    edit_userprofile.save()

                    if isinstance(user.username, unicode):
                        user.username = user.username.encode('utf-8')

                    #Grab the Site object for the context
                    site = Site.objects.get(pk=1)
                    ctx = {"site":site, "activation_key":activation_key, "expiration_days":settings.ACCOUNT_ACTIVATION_DAYS}
                    message = render_to_string(TEXTFILE_EMAIL_CHANGE_VERICATION, ctx)
                    #Keep the old email - we don't want to change the email address until it is verified, but we still send the verification email to new email address.
                    old_email = user.email
                    user.email = request.POST ["email"]
                    user.email_user(subject, message, from_email = None)
                    user.email = old_email
                    print_info_msg ("Sent email verification for %s" % user)
                    user_changed = True
                    email_changed = True

                else:
                    messages.error(request, "Sorry, the email address you provided is invalid. Try another one.")
                    return redirect (URL_EDITUSERPROFILE)

            #Check if first name has changed.
            if request.POST ["first_name"] != user.first_name:
                user.first_name = request.POST["first_name"]
                user_changed = True

            #Check if last name has changed.    
            if request.POST ["last_name"] != user.last_name:
                user.last_name = request.POST["last_name"]
                user_changed = True

            #If something about the user (or userprofile) has changed...
            if user_changed == True:
                user.save()
                user.userprofile.save()

                if email_changed == True:
                    messages.success(request, "Your changes have been saved. Please check your email to find an email from us asking to verify your new email address.")
                else:
                    messages.success(request, "Your changes have been saved.")

            return redirect(URL_USERPROFILE + str(user.userprofile.id))

        else:
            messages.error(request, "Form is not valid. Please put in properly formatted values so that EPM can update your profile.")
            return redirect(URL_EDITUSERPROFILE)
    else:
        raise Http404

@login_required
def update_User_password(request):
    if request.method == "POST":
        user = request.user
        old_password = request.POST ["old_password"]
        new_password = request.POST ["new_password"]
        confirm_password = request.POST ["confirm_password"]

        #First, check old password.
        if user.check_password(old_password) == False:
            messages.error(request, "Sorry, your old password was incorrect. Try again.")
            return redirect(URL_EDITUSERPROFILE)

        if new_password != confirm_password:
            messages.error(request, "Please confirm your new password. Your new passwords don't match.")
            return redirect(URL_EDITUSERPROFILE)

        else:
            user.set_password(new_password)
            messages.success(request, "Your password has been changed successfully.")
            user.save()
            return redirect (URL_EDITUSERPROFILE)

    else:
        raise Http404


def email_verification_complete (request, activation_key):
    '''SHA1_RE compiles the regular expression '^[a-f0-9]{40}$' 
    to search for the activation key got from the GET request'''
    SHA1_RE = re.compile('^[a-f0-9]{40}$')

    if SHA1_RE.search(activation_key):
        try:
            edituserprofile = EditUserProfile.objects.get(activation_key=activation_key)
        except:
            messages.error (request, "Sorry, that's an invalid activation key. Please try to verify your email address again.")
            return redirect(URL_USERPROFILE)

        #If OK, then save the new email for the user.
        if not edituserprofile.activation_key_expired():
            edituserprofile.user.email = edituserprofile.new_email
            edituserprofile.user.save()      
            messages.success (request, "You have successfully updated your email address!")
            edituserprofile.activation_key = "ACTIVATED"
            edituserprofile.save()

        else:
            messages.error (request, "Sorry, Your activation key has expired.")
    else:
        messages.error (request, "Your request cannot be processed at the moment, invalid activation key!")
    return redirect (URL_HOME)


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
