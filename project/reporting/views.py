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
from django.db import models, IntegrityError
from home.models import *
from django.http import Http404
from django.core import mail
from django.core.urlresolvers import reverse
from registration.forms import RegistrationForm
from random import choice, uniform
from django.contrib import messages
import re


@login_required
def submit_petreport(request):

    if request.method == "POST":
        form = PetReportForm(request.POST, request.FILES)
        print request.FILES

        if form.is_valid() == True:
            pr = form.save(commit=False)
            #Create (but do not save) the Pet Report Object associated with this form data.
            pr.proposed_by = request.user.get_profile()
            #If there was no image attached, let's take care of defaults.
            if pr.img_path == None:
                if pr.pet_type == "Dog":
                    pr.img_path.name = "images/defaults/dog_silhouette.jpg"
                elif pr.pet_type == "Cat":
                    pr.img_path.name = "images/defaults/cat_silhouette.jpg"
                elif pr.pet_type == "Horse":
                    pr.img_path.name = "images/defaults/horse_silhouette.jpg"
                elif pr.pet_type == "Rabbit":
                    pr.img_path.name = "images/defaults/rabbit_silhouette.jpg"
                elif pr.pet_type == "Snake":
                    pr.img_path.name = "images/defaults/snake_silhouette.jpg"                                       
                elif pr.pet_type == "Turtle":
                    pr.img_path.name = "images/defaults/turtle_silhouette.jpg"
                else:
                    pr.img_path.name = "images/defaults/other_silhouette.jpg"
    
            pr.save() #Now save the Pet Report.
            if pr.status == 'Lost':
                messages.success (request, 'Thank you for your submission! Your contribution will go a long way towards helping people find your lost pet.')
            else:
                messages.success (request, 'Thank you for your submission! Your contribution will go a long way towards helping others match lost and found pets.')                

            print "+++++++++++++++++++++++++ [SUCCESS]: Pet Report submitted successfully +++++++++++++++++++++++++ " 
            return redirect('/')
        else:
            print "+++++++++++++++++++++++++ [ERROR]: Pet Report not submitted successfully +++++++++++++++++++++++++ " 
            print form.errors
            print form.non_field_errors()
    else:
        form = PetReportForm() #Unbound Form

    return render_to_response('reporting/petreport_form.html', {'form':form}, RequestContext(request))

def disp_petreport(request,petreport_id):
    pet_report = PetReport.objects.get(pk = petreport_id)
    return render_to_response('reporting/petreport.html',{'pet_report': pet_report}, RequestContext(request))


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