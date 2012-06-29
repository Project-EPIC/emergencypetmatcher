# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate 
from django.contrib.auth.forms import *
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from django.db.models import Min
from social_auth import __version__ as version
from social_auth.utils import setting
from django.contrib.messages.api import get_messages
from social_auth.views import auth
from django.db import IntegrityError
from home.models import *
from django.http import Http404
from django.core import mail
from django.core.urlresolvers import reverse
from registration.forms import RegistrationForm
from random import choice, uniform
import re


@login_required
def submit_petreport(request):

    if request.method == "POST":
        form = PetReportForm(request.POST)

        if form.is_valid() == True:
            pr = form.save(commit=False)
            #Create (but do not save) the Pet Report Object associated wit this form data.
            pr.proposed_by = request.user.get_profile()
            pr.save() #Now save the Pet Report.
            if pr.status == 'Lost':
                request.session ['message'] = 'Thank you for your submission! Your contribution will go a long way towards helping people find your lost pet.'
            else:
                request.session ['message'] = 'Thank you for your submission! Your contribution will go a long way towards helping others match lost and found pets.'
            return redirect('/')
    else:
        form = PetReportForm() #Unbound Form

    return render_to_response('reporting/petreport_form.html', {'form':form}, RequestContext(request))

'''
def home(request, include_ty=False):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        if request.method == 'POST':
            return update_pet(request)
        else:
            #if uniform(0, 1) <= 1:
            #   return disp_match(request, include_ty)
            #else:
            return disp_pet(request, include_ty)
    else:
        return HttpResponse("You are currently not authenticated. Please try again.")
        #return redirect('/epm')

def disp_match(request, include_ty = False):
    candidates = Pets.objects.filter(match = None)
    candidate = choice(candidates)
    context = {'pet_id' : candidate.id, 'pet' : candidate.entries[0], 'matching' : True, 'thankyou' : include_ty}
    return render_to_response('reporting/index.html', context, RequestContext(request))

def extract_pet(request):
    pet_id = request.POST['id']
    petreport  = PetReport.objects.get(pk = pet_id)
    return petreport


def update_pet(request):
    x, new = extract_pet(request)
    matching = False
    if request.POST['matching'] == "True":
        new.lost = not new.lost
        x.match = new
        matching = True
    else:
        x.entries.append(new)
    x.save()
    return disp_pet(request, True, None)#x.id if matching else None)

def disp_pet(request, include_ty=False, oid = None):
    """grab a random pet report among those with the least revisions and upvotes"""
    x = Pets.objects.all().aggregate(Min('revisions'))['revisions__min']
    #candidates = Pets.objects.filter(revisions = x).filter(match = None)
    if oid is None:
        candidates = Pets.objects.filter(revisions = x)
    else:
        candidates = Pets.objects.filter(id = oid)
    candidate = choice(candidates)
    context = {'pet_id' : candidate.id, 'pet' : candidate.entries[-1], 'matching' : False, 'thankyou' : include_ty}
    return render_to_response('reporting/index.html', context, RequestContext(request))

def upvote(request, pet_id):
    x = Pets.objects.get(id = pet_id)
    x.entries[-1].upvotes.append(request.user.username)
    x.revisions = x.revisions + 1
    x.save()
    return redirect('/epm/reporting')
'''