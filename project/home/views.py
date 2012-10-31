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
from datetime import datetime
# from pytz import timezone

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

        # Initialize the activity list
        activities = []

        if request.user.is_authenticated() == True:

            print "Authenticated User -- recent activities..."
            current_userprofile = request.user.get_profile()      

            # Get all activities from this UserProfile's log file that show who has followed this UserProfile 
            activities += get_recent_activites_from_log(userprofile=current_userprofile, current_userprofile=current_userprofile, 
                 since_date=current_userprofile.last_logout, activity=ACTIVITY_FOLLOWER)
        
            # Get all activities that associated to the PetReports I bookmarked
            activities += get_bookmark_activities(userprofile=current_userprofile, since_date=current_userprofile.last_logout)

            # Get all activities that are associated with the UserProfiles I follow
            for following in current_userprofile.following.all().order_by("?")[:ACTIVITY_FEED_LENGTH]:
                activities += get_recent_activites_from_log(userprofile=following, current_userprofile=current_userprofile,
                    since_date=current_userprofile.last_logout) 

        else:
            print "Anonymous User -- random sample of activities..."
            # Get random activities for the anonymous user           
            for userprof in UserProfile.objects.order_by("?").filter(user__is_active=True)[:ACTIVITY_FEED_LENGTH]:
                activities += get_recent_activites_from_log(userprofile=userprof, num_activities=1)

        if len(activities) == 0:
            activities.append("<h3 style='text-align:center; color:gray;'> No Activities Yet.</h3>")
        else:
            # Sort the activity feed list according the log date
            activities.sort() 

            # Remove log date info and include only feed text 
            temp_activities = []

            activities_length = len(activities)
            if activities_length > ACTIVITY_FEED_LENGTH: activities_length = ACTIVITY_FEED_LENGTH
            for x in range(0, activities_length):
                temp_activities.append(activities[x][1])
            activities = temp_activities

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

    # Update to last_logout date field
    u = get_object_or_404(UserProfile, pk=request.user.id)
    u.last_logout = datetime.now()
    u.save()
 
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

    if request.method == 'POST':

        if request.POST.get('username'):
            request.session['saved_username'] = request.POST['username']
            backend = request.session[name]['backend']
            try:
                # Check for a duplicate username
                existing_user = User.objects.get(username=request.POST.get('username'))
                messages.error (request, "Sorry! '%s' is a duplicate username. Please try another one." % request.POST.get('username'))
                return render_to_response(HTML_SOCIAL_AUTH_FORM, {'social_detail':detail, 'pic_url':pic_url, 'link':link}, RequestContext(request))
            except:
                pass
        else:
            messages.error (request, "The username field is required.")
            return render_to_response(HTML_SOCIAL_AUTH_FORM, {'social_detail':detail, 'pic_url':pic_url, 'link':link}, RequestContext(request))

        if request.POST.get('email'):
            request.session[name]['kwargs']['details']['email'] = request.POST['email']
            backend = request.session[name]['backend']
            try:
                # Check for a duplicate email
                existing_email = User.objects.get(email=request.POST.get('email'))
                messages.error (request, "Sorry! '%s' is a duplicate email. Please try another one." % request.POST.get('email'))
                return render_to_response(HTML_SOCIAL_AUTH_FORM, {'social_detail':detail, 'pic_url':pic_url, 'link':link}, RequestContext(request))
            except:
                pass
        else:
            messages.error (request, "The email field is required.")
            return render_to_response(HTML_SOCIAL_AUTH_FORM, {'social_detail':detail, 'pic_url':pic_url, 'link':link}, RequestContext(request))

        return redirect('socialauth_complete', backend=backend)

    else:
        # If the user has logged in for the first time as facebook or twitter user
        # Get details from the associated social account
        return render_to_response(HTML_SOCIAL_AUTH_FORM, {'social_detail':detail, 'pic_url':pic_url, 'link':link}, RequestContext(request))


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
 
            # Log the following activity for this UserProfile
            log_activity(ACTIVITY_FOLLOWING, me.user.get_profile(), follow.user.get_profile())
 
    return redirect(URL_USERPROFILE + userprofile_id2)

@login_required
def unfollow(request, userprofile_id1, userprofile_id2): 
    me = get_object_or_404(UserProfile, pk=userprofile_id1) 
    unfollow = get_object_or_404(UserProfile, pk=userprofile_id2) 
    if not userprofile_id1 == userprofile_id2:
        if unfollow in me.following.all():
            me.following.remove(unfollow)
            messages.success(request, "You have successfully unfollowed '" + str(unfollow.user.username) + "'") 

            # Log the unfollowing activity for this UserProfile
            log_activity(ACTIVITY_UNFOLLOWING, me.user.get_profile(), unfollow.user.get_profile())

    return redirect(URL_USERPROFILE + userprofile_id2)

