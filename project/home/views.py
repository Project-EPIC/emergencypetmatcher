# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout, login, authenticate 
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from social_auth import __version__ as version
from social_auth.utils import setting
from django.db import IntegrityError
from home.models import *

'''Goto Home Page'''
def home (request):
    if request.user.is_authenticated():
        return render_to_response('index.html', {'user':request.user}, RequestContext(request))
    else:
        return render_to_response('index.html', RequestContext(request))

'''Goto Signup Page'''
def signup_page (request):
    return render_to_response('signup.html', RequestContext(request))

'''Goto Login Page'''
def login_page (request):
    return render_to_response('login.html', RequestContext(request))

'''Sign up user'''
def signup_user (request):
    print request.POST
    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        #Save the User to the database.
        UserProfile.objects.create(user = User.objects.create_user(username=username, email=email, password=password)) 
        return redirect('/', 
        {'info_message': 'Account registration successful. An email has been sent to your email address. Please click on the link to complete registration!'},
        RequestContext(request))

    except (IntegrityError):
        return render_to_response('/signup.html',
        {'error_message': 'An account already exists with that username. Please try another one.'}, 
        RequestContext(request))


'''Logs in user'''
def login_user (request):
    print request.POST
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username = username, password = password)
    if user is not None:
        if user.is_active == True:
            #Successful login
            login(request, user)
            return redirect('/', RequestContext(request)) 
        else:
            #Unsuccessful; account not yet activated/de-activated.
            return render_to_response('/login.html', 
             {'error_message': 'Your Account seems to be de-activated. Please login with another account, or try signing up again.'}, 
             RequestContext(request))
    else:
        #Unsuccessful - probably a wrong usernamed/password combo.
        return render_to_response('/login.html', 
            {'error_message': 'Incorrect Username/password. Please try again.'}, 
            RequestContext(request))

'''Logs out user'''
def logout_user(request):
    logout(request)
    return redirect('/', {'info_message': 'Successfully logged out.'}, RequestContext(request))    

@login_required
def done(request):
    """Login complete view, displays user data"""
    ctx = {
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
    }
    return render_to_response('home/done.html', ctx, RequestContext(request))

def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('home/error.html', {'version': version,
                                             'messages': messages},
                              RequestContext(request))

def form(request):
    if request.method == 'POST' and request.POST.get('username'):
        name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
        request.session['saved_username'] = request.POST['username']
        backend = request.session[name]['backend']
        return redirect('socialauth_complete', backend=backend)
    else:
        return render_to_response('home/form.html', {}, RequestContext(request))