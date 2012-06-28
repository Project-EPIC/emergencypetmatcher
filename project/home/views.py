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

"""Home view, displays login mechanism"""
def home (request):
    if request.user.is_authenticated():
        return social_login(request)
    else:
        pet_reports_list = PetReport.objects.all()
        return render_to_response('index.html',{'version': version, 'pet_reports_list':pet_reports_list},RequestContext(request))

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
        return render_to_response('users/login_error.html',
                                  locals(),
                                  context_instance=RequestContext(request))

@login_required
def submit_petreport(request):
    return render_to_response('reporting/petreport_form.html', {}, RequestContext(request))


@login_required
def social_login(request):
    """Login complete view, displays user data"""
    ctx = {
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
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
