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
    
    if request.user.is_authenticated():
        user = request.user.get_profile()
        if(pet_report.UserProfile_has_bookmarked(user)):
            user_has_bookmarked = "true"
            #print "user has bookmarked this petreport"
        else:
            user_has_bookmarked = "false"    
            #print "user has not bookmarked this petreport"
    else:
        user_has_bookmarked = "false"
        print "user is not authenticated" 
    return render_to_response('reporting/petreport.html',{'pet_report': pet_report,'matches': matches,'user_has_bookmarked':user_has_bookmarked}, RequestContext(request))

@login_required
def disp_bookmarks(request):

    if(request.user.is_authenticated() == False):
        raise Http404
    user = request.user.get_profile()
    pet_reports = user.bookmarks_related.all()
    paginator = Paginator(pet_reports, 100)
    page = request.GET.get('page') 
    try:
        pet_reports_list = paginator.page(page)
    except PageNotAnInteger:
        pet_reports_list = paginator.page(1)
    except EmptyPage:
        pet_reports_list = paginator.page(paginator.num_pages)        
    print len(pet_reports_list)
    return render_to_response('reporting/bookmarks.html', {'version': version, 'pet_reports_list': pet_reports_list, 'last_login': request.session.get('social_auth_last_login_backend')}, RequestContext(request))
    
'''AJAX Request to bookmark a PetReport'''
@login_required
def bookmark_PetReport(request):

    if request.method == "POST":
        user = request.user.get_profile()
        petreport_id = request.POST['petreport_id']
        petreport = get_object_or_404(PetReport, pk = petreport_id)
        action = request.POST['action']
        #print "path: "+str(request.META.get('HTTP_REFERER','/'))
        if ((petreport.UserProfile_has_bookmarked(user)) and (action == "Remove Bookmark")) :
            petreport.bookmarked_by.remove(user)
            petreport.save()
            message = "You have successfully removed the bookmark for this Pet Report." 
            text = "Bookmark this Pet"
        elif ((not petreport.UserProfile_has_bookmarked(user)) and (action == "Bookmark this Pet")):
            petreport.bookmarked_by.add(user)
            petreport.save()
            print 'Bookmarked pet report #'+str(petreport_id)+" for user #"+str(user.id)
            message = "You have successfully bookmarked this Pet Report!" 
            text = "Remove Bookmark"
        else:
            print "User has bookmarked the pet: "+str(petreport.UserProfile_has_bookmarked(user))
            message = "Unable to "+action
            text = action
        json = simplejson.dumps ({"message":message, "text":text})
        print "JSON: " + str(json)
        return HttpResponse(json, mimetype="application/json")
    else:
        raise Http404
    
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



