# Create your views here.
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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import simplejson
from home.models import *
from constants import *
from logging import *
import oauth2 as oauth, random, urllib
from django.forms.models import model_to_dict
import utils
import hashlib,random,re
from registration.models import RegistrationProfile
from django.template.loader import render_to_string
from django.conf import settings

"""Home view, displays login mechanism"""
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

    print "======= AJAX: get_activities_json ========="
    if request.is_ajax() == True:
        #Let's populate the activity feed based upon whether the user is logged in.
        activities = []

        if request.user.is_authenticated() == True:

            print "Authenticated User -- following sample of activities..."
            userprofile = request.user.get_profile()

            for following in userprofile.following.all().order_by("?")[:ACTIVITY_FEED_LENGTH]:
                activities.append(get_recent_log(following))

        else:
            print "Anonymous User -- random sample of activities..."
            for userprof in UserProfile.objects.order_by("?").filter(user__is_active=True)[:ACTIVITY_FEED_LENGTH]:
                print userprof
                activities.append(get_recent_log(userprof))

        if len(activities) == 0:
            activities.append("<h3 style='text-align:center; color:gray;'> No Activities Yet.</h3>")

        json = simplejson.dumps ({"activities":activities})
        print "JSON: " + str(json)
        return HttpResponse(json, mimetype="application/json")                


def login_User(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, 'Welcome, %s!' % (username))
                log_activity(ACTIVITY_LOGIN, user.get_profile())
                return redirect(request.REQUEST ['next'])

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
    if request.method == 'POST':
        user = UserProfile.objects.get(pk = request.user.id).user        
        if request.POST["action"] == 'saveProfile':         
            edit_userprofile_form = UserProfileForm(request.POST)
            print "[DEBUGGING]: "+str(edit_userprofile_form.errors)
            if edit_userprofile_form.is_valid():
                user.username = request.POST["username"]
                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.save()
                if user.email != request.POST["email"]:
                    #USE CONSTANTS
                    subject = render_to_string("registration/activation_email_subject.txt")
                    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
                    username = user.username
                    if isinstance(username, unicode):
                        username = username.encode('utf-8')
                    activation_key = hashlib.sha1(salt+username).hexdigest()
                    print 'user: %s \tactivation-key: %s' % (user,activation_key)
                    try:
                        edit_userprofile = EditUserProfile.objects.get(user=user)
                        edit_userprofile.activation_key = activation_key
                    except:
                        edit_userprofile = EditUserProfile.objects.create(user=user,activation_key=activation_key)                  
                    edit_userprofile.new_email = request.POST["email"]
                    edit_userprofile.save()
                    ctx = {"activation_key":activation_key,"expiration_days":settings.ACCOUNT_ACTIVATION_DAYS}
                    message = render_to_string("home/email_change_verification.txt",ctx)
                    user.email = request.POST["email"]
                    user.email_user(subject, message, from_email = None)
                    print "[INFO]: sent email verification"              
                message = "<li class='success'>Your changes have been saved!</li>"
            else:
                message = str(edit_userprofile_form.errors)
           #distinguish bet social user &  registered user. no password change for social auth users 
        elif request.POST["action"] == 'savePassword':
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
    else:
        user = request.user
        form = UserProfileForm(initial={'first_name': user.first_name,'last_name': user.last_name,'username':user.username,'email':user.email})
        form1 = []
        form2 = []
        for field in form:
            if 'password' in field.name:
                form2.append(field)
            else:
                form1.append(field)
        if (user.social_auth == []):
            form2 = []
        return render_to_response('home/EditUserProfile_form.html', {'form1':form1,'form2':form2}, RequestContext(request))

def email_verification_complete (request,activation_key):
    '''1.check if activation_key is correct & valid
    2. change email address on auth_user table
    3.save it.'''
    SHA1_RE = re.compile('^[a-f0-9]{40}$')
    if SHA1_RE.search(activation_key):
        try:
            profile = EditUserProfile.objects.get(activation_key=activation_key)
        except:
            return False
        #if not profile.activation_key_expired():
        profile.user.email = profile.new_email
        profile.user.save()      
        messages.success (request, "You have successfully updated your email!")
    else:
        messages.error (request, "Your request cannot be processed at the moment, invalid activation key!")
    return redirect (URL_HOME)