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
from django.http import Http404
from django.core import mail
from django.core.urlresolvers import reverse
from registration.forms import RegistrationForm
from random import choice, uniform
from django.contrib import messages
from django.utils import simplejson
from matching.views import *
from django.forms.models import model_to_dict
from django.contrib.sites.models import Site
from social.models import UserProfile
from reporting.models import PetReport, PetReportForm
from matching.models import PetMatch
from pprint import pprint
from PIL import Image
from utilities import logger
from utilities.utils import *
from constants import *
from home.constants import *
import datetime, re, time

@login_required
def submit_PetReport(request):
    if request.method == "POST":

        #Let's make some adjustments to non-textual form fields before converting to a PetReportForm.
        geo_lat = request.POST ["geo_location_lat"] or ""
        geo_long = request.POST ["geo_location_long"] or ""

        if (geo_lat == "" or geo_lat == "None") or (geo_long == "" or geo_long == "None"):
            request.POST ['geo_location_lat'] = 0.00
            request.POST ['geo_location_long'] = 0.00

        pprint(request.POST)
        form = PetReportForm(request.POST, request.FILES)

        if form.is_valid() == True:
            pr = form.save(commit=False)
            #Create (but do not save) the Pet Report Object associated with this form data.
            pr.proposed_by = request.user.get_profile()
            img_rotation = 0

            #if email_re.match(pr.contact_email) == None:
            
            #Deal with Contact Information.
            if pr.contact_name.strip() == "":
                pr.contact_name = None
            if pr.contact_email.strip() == "":
                pr.contact_email = None
            if pr.contact_number.strip() == "":
                pr.contact_number = None
            if pr.contact_link.strip() == "":
                pr.contact_link = None

            if request.POST.get("img_rotation") != None:
                img_rotation = - int(request.POST ["img_rotation"])

            print_info_msg ("Pet Report Image Path: %s" % pr.img_path)

            #Make and save images from img_path and thumb_path AND save the PetReport.
            pr.set_images(pr.img_path, save=True, rotation=img_rotation)

            #Add reputation points for submitting a pet report
            request.user.get_profile().update_reputation(ACTIVITY_PETREPORT_SUBMITTED)
            if pr.status == 'Lost':
                messages.success (request, 'Thank you for your submission! Your contribution will go a long way towards helping people find your lost pet.')
            else:
                messages.success (request, 'Thank you for your submission! Your contribution will go a long way towards helping others match lost and found pets.')                

            #Log the PetReport submission for this UserProfile
            logger.log_activity(ACTIVITY_PETREPORT_SUBMITTED, request.user.get_profile(), petreport=pr)
            print_success_msg("Pet Report submitted successfully")
            return redirect(URL_HOME)

        else:
            print_error_msg ("Pet Report not submitted successfully")
            print_error_msg (form.errors)
            print_error_msg (form.non_field_errors())
            return render_to_response(HTML_SUBMIT_PETREPORT, {  'form':form,
                                                                "PETREPORT_TAG_INFO_LENGTH":PETREPORT_TAG_INFO_LENGTH, 
                                                                "PETREPORT_DESCRIPTION_LENGTH":PETREPORT_DESCRIPTION_LENGTH,
                                                                "PETREPORT_CONTACT_NAME_LENGTH": PETREPORT_CONTACT_NAME_LENGTH,
                                                                "PETREPORT_CONTACT_NUMBER_LENGTH": PETREPORT_CONTACT_NUMBER_LENGTH,
                                                                "PETREPORT_CONTACT_EMAIL_LENGTH": PETREPORT_CONTACT_EMAIL_LENGTH,
                                                                "PETREPORT_CONTACT_LINK_LENGTH": PETREPORT_CONTACT_LINK_LENGTH }, RequestContext(request))
    else:
        form = PetReportForm() #Unbound Form
    return render_to_response(HTML_SUBMIT_PETREPORT, {  'form':form,
                                                        "PETREPORT_TAG_INFO_LENGTH":PETREPORT_TAG_INFO_LENGTH, 
                                                        "PETREPORT_DESCRIPTION_LENGTH":PETREPORT_DESCRIPTION_LENGTH,
                                                        "PETREPORT_CONTACT_NAME_LENGTH": PETREPORT_CONTACT_NAME_LENGTH,
                                                        "PETREPORT_CONTACT_NUMBER_LENGTH": PETREPORT_CONTACT_NUMBER_LENGTH,
                                                        "PETREPORT_CONTACT_EMAIL_LENGTH": PETREPORT_CONTACT_EMAIL_LENGTH,
                                                        "PETREPORT_CONTACT_LINK_LENGTH": PETREPORT_CONTACT_LINK_LENGTH }, RequestContext(request))

@login_required
def get_pet_breeds(request, pet_type=0):
    if request.is_ajax() == True:
        if pet_type == "0":
            f = PETREPORT_BREED_DOG_FILE
        elif pet_type == "1":
            f = PETREPORT_BREED_CAT_FILE
        elif pet_type == "2":
            f = PETREPORT_BREED_HORSE_FILE
        elif pet_type == "3":
            f = PETREPORT_BREED_BIRD_FILE
        elif pet_type == "4":
            f = PETREPORT_BREED_RABBIT_FILE
        elif pet_type == "5":
            f = PETREPORT_BREED_TURTLE_FILE
        elif pet_type == "6":
            f = PETREPORT_BREED_SNAKE_FILE
        #If Other, Load Other Breeds (Nothing)
        elif pet_type == "7":
            f = PETREPORT_BREED_OTHER_FILE
        else:
            return HttpResponse("", mimetype="application/json") #nothing to return.

        with open(f) as read_file:
            data = read_file.readlines()

        breeds = []
        for index, breed in enumerate(data):
            breeds.append({"id":breed, "text":breed})

        json = simplejson.dumps({"breeds":breeds})
        return HttpResponse(json, mimetype="application/json")

    else:
        raise Http404

    
def get_PetReport(request, petreport_id):
    #Grab the PetReport.
    pet_report = get_object_or_404(PetReport, pk = petreport_id)
    user_has_bookmarked = False

    #Get all PetMatches made already for this PetReport object.
    if pet_report.status == 'Lost':
        matches = PetMatch.objects.all().filter(lost_pet = pet_report)
    else:
        matches = PetMatch.objects.all().filter(found_pet = pet_report)

    #Grab number of workers for this PetReport
    num_workers = len(pet_report.workers.all())
    if request.user.is_authenticated() == True:
        user_is_worker = pet_report.UserProfile_is_worker(request.user.userprofile)
    else:
        user_is_worker = False
    
    if request.user.is_authenticated() == True:
        userprofile = request.user.get_profile()

        if pet_report.UserProfile_has_bookmarked(userprofile) == True:
            user_has_bookmarked = True

    #Serialize the PetReport into JSON for easy accessing.
    pr_json = pet_report.toJSON()
    return render_to_response(HTML_PRDP, {  'pet_report_json':pr_json, 
                                            'pet_report': pet_report,
                                            'site_domain': Site.objects.get_current().domain,
                                            'num_workers':num_workers,
                                            'user_is_worker':user_is_worker, 
                                            'matches': matches,
                                            'user_has_bookmarked':user_has_bookmarked}, 
                                            RequestContext(request))
#AJAX Request to bookmark a PetReport
@login_required
def bookmark_PetReport(request):
    if request.method == "POST" and request.is_ajax() == True:
        user = request.user.get_profile()
        petreport_id = request.POST['petreport_id']
        petreport = get_object_or_404(PetReport, pk=petreport_id)
        action = request.POST['action']
        print_debug_msg("User: %s, Action: %s, petreport: %s" % (request.user.username, action, petreport))

        #If the user has bookmarked this pet and the action is to remove it...
        if ((petreport.UserProfile_has_bookmarked(user)) and (action == "Remove Bookmark")) :
            petreport.bookmarked_by.remove(user)
            petreport.save()
            user.update_reputation(ACTIVITY_PETREPORT_REMOVE_BOOKMARK)
            message = "You have successfully removed the bookmark for this pet." 
            text = "Bookmark this Pet"

            # Log removing the PetReport bookmark for this UserProfile
            logger.log_activity(ACTIVITY_PETREPORT_REMOVE_BOOKMARK, request.user.get_profile(), petreport=petreport)

        #If the user has NOT bookmarked this pet and the action is to bookmark it...
        elif ((not petreport.UserProfile_has_bookmarked(user)) and (action == "Bookmark this Pet")):
            petreport.bookmarked_by.add(user)
            petreport.save()
            user.update_reputation(ACTIVITY_PETREPORT_ADD_BOOKMARK)
            print_info_msg ('Bookmarked pet report %s for %s' % (petreport, user))
            message = "You have successfully bookmarked this pet!" 
            text = "Remove Bookmark"

            # Log adding the PetReport bookmark for this UserProfile
            logger.log_activity(ACTIVITY_PETREPORT_ADD_BOOKMARK, request.user.get_profile(), petreport=petreport)

        else:
            print_info_msg ("User has bookmarked the pet: " + str(petreport.UserProfile_has_bookmarked(user)))
            message = "Unable to "+action+"!"
            text = action
        json = simplejson.dumps ({"message":message, "text":text})
        #print "JSON: " + str(json)
        return HttpResponse(json, mimetype="application/json")
    else:
        raise Http404


