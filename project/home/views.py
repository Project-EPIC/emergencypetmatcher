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
from home.models import *
from django.http import Http404
from django.core import mail
from django.core.urlresolvers import reverse
from registration.forms import RegistrationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.contrib import messages
import urllib
import oauth2 as oauth

"""Home view, displays login mechanism"""
def home (request):
    #Get Pet Report objects and organize them into a Paginator Object.
    pet_reports = PetReport.objects.all()
    paginator = Paginator(pet_reports, 100)
    page = request.GET.get('page')
    
    try:
        pet_reports_list = paginator.page(page)
    except PageNotAnInteger:
        pet_reports_list = paginator.page(1)
    except EmptyPage:
        pet_reports_list = paginator.page(paginator.num_pages)
        
    if request.user.is_authenticated():
        return social_login(request, pet_reports_list)
    else:
        return render_to_response('index.html', {'version': version, 'pet_reports_list': pet_reports_list}, RequestContext(request))

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                redirect_to = request.REQUEST ['next']
                messages.success(request, 'Welcome, %s!' % (username))
                return redirect(redirect_to)

            else:
                messages.error(request, 'There seems to be a problem with the account. Please try re-registering.')
                
        else:
            messages.error(request, 'Invalid Login credentials. Please try again.')
    
    try: 
        next = request.REQUEST ['next']
    except KeyError: #This only happens if the user tries to plug in the login URL without a 'next' parameter...
        next = '/'

    form = AuthenticationForm()
    return render_to_response('registration/login.html', {'form':form}, RequestContext(request, {'next': next}))


def logout_user(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('/')

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
        return render_to_response('registration/social_auth_username_form.html', locals(), RequestContext(request))
    except ValueError, error:
        # in case of errors, let's show a special page that will explain what happened
        return render_to_response('registration/login_errors.html', locals(), context_instance=RequestContext(request))

@login_required
def social_login(request,pet_reports_list):
    """Login complete view, displays user data"""
    ctx = {
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend'),
        'pet_reports_list': pet_reports_list
    }
    return render_to_response('index.html', ctx, RequestContext(request))


''' Used by social auth pipeline  
    to get a username value when authenticate a social user for the first time '''
def form(request):
    if request.method == 'POST' and request.POST.get('username'):
        name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
        request.session['saved_username'] = request.POST['username']
        backend = request.session[name]['backend']
        return redirect('socialauth_complete', backend=backend)
    else:
        return render_to_response('registration/social_auth_username_form.html', {}, RequestContext(request))

@login_required
def detail(request, userprofile_id):   
    u = get_object_or_404(UserProfile, pk=userprofile_id) 
    return render_to_response('detail.html', {'userprofile':u}, context_instance=RequestContext(request))
 
@login_required
def share(request, petreport_id): 
    p = get_object_or_404(PetReport, pk=petreport_id) 
    u = p.proposed_by

    # To be completed
    
    return render_to_response('detail.html', {'userprofile':u}, context_instance=RequestContext(request))

