from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout, login, authenticate 
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import *
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from social_auth import __version__ as version
from social_auth.utils import setting
from social_auth.views import auth
from django.db import IntegrityError
from django.http import Http404
from django.core import mail
from django.core.urlresolvers import reverse
from registration.forms import RegistrationForm
from django.forms.models import model_to_dict
from registration.models import RegistrationProfile
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.timezone import now as datetime_now
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import simplejson
from home.models import *
from constants import *
from logging import *
from registration import *
from utils import *
import oauth2 as oauth, random, urllib
import hashlib, random, re

#Home view, displays login mechanism
def home (request):
    #Get Pet Report objects and organize them into a Paginator Object.
    pet_reports = PetReport.objects.order_by("id").reverse()
    paginator = Paginator(pet_reports, 50)
    page = request.GET.get('page')
    
    try:
        pet_reports_list = paginator.page(page)
    except PageNotAnInteger:
        pet_reports_list = paginator.page(1)
    except EmptyPage:
        pet_reports_list = paginator.page(paginator.num_pages)

    if request.user.is_authenticated() == True:
        return render_to_response(HTML_HOME, {'pet_reports_list': pet_reports_list, 'last_login': request.session.get('social_auth_last_login_backend'), 'version':version}, RequestContext(request))

    else:
        return render_to_response(HTML_HOME, {'pet_reports_list': pet_reports_list, 'version': version}, RequestContext(request))

def get_activities_json(request):
    print "======= [AJAX]: get_activities_json ========="

    if request.is_ajax() == True:
        #Let's populate the activity feed based upon whether the user is logged in.
        activities = []

        if request.user.is_authenticated() == True:
            print "[INFO]: get_activities_json(): Authenticated User -- following sample of activities..."
            userprofile = request.user.get_profile()

            for following in userprofile.following.all().order_by("?")[:ACTIVITY_FEED_LENGTH]:
                log = get_recent_log(following)

                if log != None:
                    activities.append(log)

        else:
            print "[INFO]: get_activities_json(): Anonymous User -- random sample of activities..."

            for userprof in UserProfile.objects.order_by("?").filter(user__is_active=True)[:ACTIVITY_FEED_LENGTH]:
                log = get_recent_log(userprof)

                if log != None:
                    activities.append(log)

        #If there are no activities, let the user know!
        if len(activities) == 0:
            activities.append("<h3 style='text-align:center; color:gray;'> No Activities Yet.</h3>")

        #ERROR message print to flag for potential problem in the log directory.
        if request.user.is_authenticated() == False and len(activities) != ACTIVITY_FEED_LENGTH:
            print "[ERROR]: Length of activity list is %d when it should be ACTIVITY_FEED_LENGTH = %d" % (len(activities), ACTIVITY_FEED_LENGTH)

        print "======= END [AJAX]: get_activities_json =========\n"
        #Zip it up in JSON and ship it out as an HTTP Response.
        json = simplejson.dumps ({"activities":activities})
        return HttpResponse(json, mimetype="application/json")     

    else:
        print "[ERROR]: Request for get_activities_json not an AJAX request!"
        raise Http404           


def login_User(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user != None:
            if user.is_active == True:
                userprofile = user.get_profile()

                if log_exists(userprofile) == False:
                    log_activity(ACTIVITY_ACCOUNT_CREATED, userprofile)

                login(request, user)
                messages.success(request, 'Welcome, %s!' % (username))
                log_activity(ACTIVITY_LOGIN, user.get_profile())
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
    messages.success(request, "You have successfully logged out.")
    log_activity(ACTIVITY_LOGOUT, request.user.get_profile())
    logout(request)
    return redirect(URL_HOME)

def registration_activation_complete (request):
    print request
    messages.success (request, "Alright, you are all set registering! You may now login to the system.")
    return redirect (URL_LOGIN)

def registration_complete (request):
    messages.success (request, "Thanks for registering for EPM. Look for an account verification email and click on the link to finish registering.")
    return home(request)

def registration_disallowed (request):
    messages.error (request, "Sorry, we are not accepting registrations at this time. Please try again later.")
    return home(request)

def social_auth_login(request, backend):
    """
        This view is a wrapper to social_auths auth
        It is required, because social_auth just throws ValueError and gets user to 500 error
        after every unexpected action. This view handles exceptions in human friendly way.
        See https://convore.com/django-social-auth/best-way-to-handle-exceptions/
    """
    try:
        # if everything is ok, then original view gets returned, no problem
        return auth(request, backend)
    except IntegrityError, error:
        return render_to_response(HTML_SOCIAL_AUTH_FORM, locals(), RequestContext(request))


''' Used by social auth pipeline  
    to get a username value when authenticate a social user for the first time '''
def form(request):
    if request.method == 'POST' and request.POST.get('username'):
        name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
        request.session['saved_username'] = request.POST['username']
        backend = request.session[name]['backend']
        return redirect('socialauth_complete', backend=backend)
    else:
        return render_to_response(HTML_SOCIAL_AUTH_FORM, {}, RequestContext(request))

@login_required
def get_UserProfile_page(request, userprofile_id):   
    u = get_object_or_404(UserProfile, pk=userprofile_id)
    return render_to_response(HTML_USERPROFILE, {'show_profile':u}, RequestContext(request))
 
@login_required
def follow(request, userprofile_id1, userprofile_id2): 
    me = get_object_or_404(UserProfile, pk=userprofile_id1) 
    follow = get_object_or_404(UserProfile, pk=userprofile_id2) 
    if not userprofile_id1 == userprofile_id2:
        if follow in me.following.all():
            messages.success(request, "You are already following '" + str(follow.user.username) + "'")        
        else:
            me.following.add(follow)
            messages.success(request, "You have successfully followed '" + str(follow.user.username) + "'") 
    return redirect('/UserProfile/' + userprofile_id1)

@login_required
def unfollow(request, userprofile_id1, userprofile_id2): 
    me = get_object_or_404(UserProfile, pk=userprofile_id1) 
    unfollow = get_object_or_404(UserProfile, pk=userprofile_id2) 
    if not userprofile_id1 == userprofile_id2:
        if unfollow in me.following.all():
            me.following.remove(unfollow)
            messages.success(request, "You have successfully unfollowed '" + str(unfollow.user.username) + "'") 
    return redirect('/UserProfile/' + userprofile_id1)

@login_required
def editUserProfile_page(request):
    '''unhandled issue: invalid email address'''
    if request.method == 'POST':
        user = UserProfile.objects.get(pk = request.user.id).user        
        '''SaveProfile workflow will be executed if the user clicks on "save" after editing
        first_name, last_name, email or username'''
        if request.POST["action"] == 'saveProfile':         
            user_changed = False
            edit_userprofile_form = UserProfileForm(request.POST,request.FILES)
            if edit_userprofile_form.is_valid():
                if request.POST["username"] != user.username:
                    user.username = request.POST["username"]
                    try:
                        user.save()
                        user_changed = True
                    except:
                        message = "<li class='error'>This username is  unavailable, please try another one.</li>"
                        json = simplejson.dumps ({"message":message})
                        print "JSON: " + str(json)
                        return HttpResponse(json, mimetype="application/json")

                if user.first_name != request.POST["first_name"]:
                    user.first_name = request.POST["first_name"]
                    user_changed = True
                if user.last_name != request.POST["last_name"]:
                    user.last_name = request.POST["last_name"]
                    user_changed = True
                if user_changed:
                    try:
                        user.save()
                        message = "<li class='success'>Thank you. Your changes have been saved!</li>"
                    except:
                        print "Error while saving your changes, please try again!"      
                        message = "<li class='error'>unknown error while  saving</li>"                  
                    
                if user.email != request.POST["email"]:
                    
                    user_changed = True
                    subject = render_to_string(TEXTFILE_EMAIL_ACTIVATION_SUBJECT)
                    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
                    username = user.username
                    if isinstance(username, unicode):
                        username = username.encode('utf-8')
                    activation_key = hashlib.sha1(salt+username).hexdigest()
                    print 'user: %s \tactivation-key: %s' % (user,activation_key)
                    try:
                        edit_userprofile = EditUserProfile.objects.get(user=user)
                        edit_userprofile.activation_key = activation_key
                    except EditUserProfile.DoesNotExist:
                        edit_userprofile = EditUserProfile.objects.create(user=user,activation_key=activation_key)
                    edit_userprofile.new_email = request.POST["email"]
                    edit_userprofile.date_of_change = datetime_now()
                    edit_userprofile.save()
                    ctx = {"activation_key":activation_key,"expiration_days":settings.ACCOUNT_ACTIVATION_DAYS}
                    message = render_to_string(TEXTFILE_EMAIL_CHANGE_VERICATION,ctx)
                    user.email = request.POST["email"]
                    user.email_user(subject, message, from_email = None)
                    print "[INFO]: sent email verification"              
                    message = "<li class='success'>Thank you. Your changes have been saved! Your email will be updated once you verify it. Please check your email for more information on how to verify.</li>"
                if not user_changed:
                    '''If user does not make any changes to his profile then this message is sent back'''
                    message = "<li class='error'>No changes were made.</li>"
            else:
                '''If UserProfileForm is invalid then the errors will be sent as a message 
                which will be displayed as an error message'''
                message = str(edit_userprofile_form.errors)

        elif request.POST["action"] == 'savePassword':
            '''savePassword workflow will be executed if the user clicks on "submit" after 
            changing the password'''
            old_password = request.POST["old_password"]
            new_password = request.POST["new_password"]
            confirm_password = request.POST["confirm_password"]
            if not user.check_password(old_password):
                message = "<li class='error'>Sorry, your password was incorrect!</li>"
            elif new_password != confirm_password:
                message = "<li class='error'>Please confirm your new password. Your new passwords do not match!</li>"
            else:
                user.set_password(new_password)  
                message = "<li class='success'>Congratulations! Your password has been changed successfully.</li>"
                user.save()  
        json = simplejson.dumps ({"message":message})
        print "JSON: " + str(json)
        return HttpResponse(json, mimetype="application/json")
    elif request.method=='GET':
        user = request.user
        form = UserProfileForm(initial={'first_name': user.first_name,'last_name': user.last_name,'username':user.username,'email':user.email})
        ''' form1 is the form used for "saveProfile", form2 is used for "savePassword"'''
        form1 = []
        form2 = []
        ''''form2 shouldn't be shown to social_auth users 
        because they can't change their passwords '''
        if user.social_auth.count() == 0:
            social_auth_user = "false"
        else:
            social_auth_user = "true"

        for field in form:
            if 'password' in field.name:
                form2.append(field)
            else:
                form1.append(field)
        photo = str(user.get_profile().photo)
        return render_to_response(HTML_EDITUSERPROFILE_FORM, {'form1':form1,'form2':form2,'social_auth_user':social_auth_user,"profile_picture":photo}, RequestContext(request))
    else:
        return Http404()

def email_verification_complete (request,activation_key):
    '''SHA1_RE compiles the regular expression '^[a-f0-9]{40}$' 
    to search for the activation key got from the GET request'''
    SHA1_RE = re.compile('^[a-f0-9]{40}$')

    if SHA1_RE.search(activation_key):
        try:
            edituserprofile = EditUserProfile.objects.get(activation_key=activation_key)
        except:
            messages.error (request, "Invalid Activation Key!")
            return False
        if not edituserprofile.activation_key_expired():
            edituserprofile.user.email = edituserprofile.new_email
            edituserprofile.user.save()      
            messages.success (request, "You have successfully updated your email!")
            edituserprofile.activation_key = "ACTIVATED"
            edituserprofile.save()
        else:
            messages.error (request, "Sorry, Your activation key has expired.")
    else:
        messages.error (request, "Your request cannot be processed at the moment, invalid activation key!")
    return redirect (URL_HOME)
