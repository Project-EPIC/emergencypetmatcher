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
from django.utils import simplejson
from django.core import serializers
from matching.views import *
from django.forms.models import model_to_dict
import utils
import datetime, re

@login_required
def submit_PetReport(request):

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

            #Log the PetReport submission for this UserProfile
            log_activity(ACTIVITY_PETREPORT_SUBMITTED, request.user.get_profile(), petreport=pr)
            print "[SUCCESS]: Pet Report submitted successfully" 
            return redirect('/')

        else:
            print "[ERROR]: Pet Report not submitted successfully" 
            print form.errors
            print form.non_field_errors()
    else:
        form = PetReportForm() #Unbound Form

    return render_to_response('reporting/petreport_form.html', {'form':form}, RequestContext(request))

def disp_PetReport(request, petreport_id):

    pet_report = get_object_or_404(PetReport, pk = petreport_id)

    if pet_report.status == 'Lost':
        matches = PetMatch.objects.all().filter(lost_pet = pet_report)
    else:
        matches = PetMatch.objects.all().filter(found_pet = pet_report)

    return render_to_response('reporting/petreport.html',{'pet_report': pet_report,'matches': matches}, RequestContext(request))


@login_required
def bookmark_PetReport(request):

    if request.method == "POST":
        user_id = request.POST['user_id']
        petreport_id = request.POST['petreport_id']
        print 'Bookmarking petreport #'+str(petreport_id)+" for user #"+str(user_id)
        user = UserProfile.objects.get(pk = user_id)
        pet_report = PetReport.objects.get(pk = petreport_id)
    else:
        print 'did not receive a post request'    
    return HttpResponse()

'''AJAX Request to retrieve a PetReport object in JSON format'''
def get_PetReport_json(request, petreport_id):

    if request.is_ajax() == True:
        print "============== AJAX REQUEST ======================= "
        prdp = get_object_or_404(PetReport, pk=petreport_id)

        #Need this for easy displaying on the Matching Interface workspace detail table.
        prdp_dict = utils.simplify_model_dict(prdp) 

        json = simplejson.dumps(prdp_dict)
        print "JSON: " + str(json)
        return HttpResponse(json, mimetype="application/json")

    print "Oops,something went wrong"
    messages.failure(request, "Oops, something went wrong.")
    return matching.match_petreport(request, petreport_id)



