from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate 
from django.contrib.auth.forms import *
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from django.db.models import Min
from django.contrib.messages.api import get_messages
from django.db import models, IntegrityError
from django.http import Http404
from django.core import mail
from django.core.urlresolvers import reverse
from registration.forms import RegistrationForm
from random import choice, uniform
from django.contrib import messages
from matching.views import *
from django.conf import settings
from django.forms.models import model_to_dict
from django.contrib.sites.models import Site
from home.models import Activity
from socializing.models import UserProfile
from reporting.models import PetReport, PetReportForm
from matching.models import PetMatch
from pprint import pprint
from PIL import Image
from utilities.utils import *
from constants import *
from home.constants import *
import datetime, re, time, json, pdb, urllib, urllib2

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

    if UserProfile.get_UserProfile(username=request.user.username) and (pet_report.proposed_by == request.user.userprofile):
        edit_petreport = True
    else:
        edit_petreport = False        
    
    if request.user.is_authenticated() == True:
        userprofile = request.user.userprofile

        if pet_report.UserProfile_has_bookmarked(userprofile) == True:
            user_has_bookmarked = True

    pet_has_been_successfully_matched = pet_report.has_been_successfully_matched()
    if pet_has_been_successfully_matched == True:
        messages.success(request, "This pet has been successfully matched with its owner! Thank you digital volunteers!")

    if request.is_ajax() == True:
        html = HTML_PRDP
    else:
        html = HTML_PRDP_FULL

    return render_to_response(html, {
        'pet_report': pet_report,
        'petreport_fields': pet_report.get_display_fields(),
        'edit_petreport': edit_petreport,
        'pet_has_been_successfully_matched': pet_has_been_successfully_matched,
        'site_domain': Site.objects.get_current().domain,
        'num_workers':num_workers,
        'user_is_worker':user_is_worker, 
        'matches': matches,
        'user_has_bookmarked':user_has_bookmarked 
    }, RequestContext(request))


@login_required
def submit(request):
    if request.method == "POST" and request.POST["g-recaptcha-response"]:
        recaptcha = request.POST["g-recaptcha-response"]
        query_data = urllib.urlencode({"secret":settings.RECAPTCHA_SERVER_SECRET, "response":recaptcha})
        response = urllib2.urlopen(settings.RECAPTCHA_SITEVERIFY, query_data)
        status = json.loads(response.read())

        if status["success"] != True:
            messages.error(request, "CAPTCHA was not correct. Please try again.")
            return redirect(URL_SUBMIT_PETREPORT)

        #Let's make some adjustments to non-textual form fields before converting to a PetReportForm.
        geo_lat = request.POST ["geo_location_lat"] or ""
        geo_long = request.POST ["geo_location_long"] or ""

        if (geo_lat == "" or geo_lat == "None") or (geo_long == "" or geo_long == "None"):
            request.POST ['geo_location_lat'] = 0.00
            request.POST ['geo_location_long'] = 0.00
        else:
            request.POST ["geo_location_lat"] = float("%.5f" % float(geo_lat))
            request.POST ["geo_location_long"] = float("%.5f" % float(geo_long))

        form = PetReportForm(request.POST, request.FILES)

        if form.is_valid() == True:
            pr = form.save(commit=False)
            #Create (but do not save) the Pet Report Object associated with this form data.
            pr.proposed_by = request.user.userprofile
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

            print_info_msg ("Pet Report Image Path: %s" % pr.img_path)

            #Make and save images from img_path and thumb_path AND save the PetReport.
            pr.set_images(pr.img_path, save=True, rotation=request.POST.get("img_rotation"))

            #Add reputation points for submitting a pet report
            request.user.userprofile.update_reputation("ACTIVITY_PETREPORT_SUBMITTED")
            message = "Thank you for your submission! You have earned %d Pet Points! " % ACTIVITIES["ACTIVITY_PETREPORT_SUBMITTED"]["reward"]
            if pr.status == 'Lost':
                messages.success (request, message + "Your contribution will go a long way towards helping people find your lost pet.")
            else:
                messages.success (request, message + "Your contribution will go a long way towards helping others match lost and found pets.")                

            #Log the PetReport submission for this UserProfile
            Activity.log_activity("ACTIVITY_PETREPORT_SUBMITTED", request.user.userprofile, source=pr)
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
        if request.method == "POST" and not request.POST["g-recaptcha-response"]:
            messages.error (request, "Please fill in the RECAPTCHA.")        
        form = PetReportForm() #Unbound Form

    return render_to_response(HTML_SUBMIT_PETREPORT, {  
        'form':form,
        "RECAPTCHA_CLIENT_SECRET": settings.RECAPTCHA_CLIENT_SECRET,
        "PETREPORT_TAG_INFO_LENGTH":PETREPORT_TAG_INFO_LENGTH, 
        "PETREPORT_DESCRIPTION_LENGTH":PETREPORT_DESCRIPTION_LENGTH,
        "PETREPORT_CONTACT_NAME_LENGTH": PETREPORT_CONTACT_NAME_LENGTH,
        "PETREPORT_CONTACT_NUMBER_LENGTH": PETREPORT_CONTACT_NUMBER_LENGTH,
        "PETREPORT_CONTACT_EMAIL_LENGTH": PETREPORT_CONTACT_EMAIL_LENGTH,
        "PETREPORT_CONTACT_LINK_LENGTH": PETREPORT_CONTACT_LINK_LENGTH 
    }, RequestContext(request))


@login_required 
def edit(request, petreport_id):
    pet_report = get_object_or_404(PetReport, pk=petreport_id)
    if request.method == "GET":
        form = PetReportForm(instance=pet_report)

    elif request.method == "POST":
        form = PetReportForm(request.POST, request.FILES)
        if form.is_valid() == True:
            pr = form.save(commit=False)
            pet_report.update_fields(pr, request=request.POST)
            messages.success(request, "You've successfully updated your pet report.")
            return redirect(URL_HOME)
    else:
        raise Http404

    return render_to_response(HTML_EDIT_PETREPORT, {
        "form": form,
        "petreport": pet_report,
        "PETREPORT_TAG_INFO_LENGTH":PETREPORT_TAG_INFO_LENGTH, 
        "PETREPORT_DESCRIPTION_LENGTH":PETREPORT_DESCRIPTION_LENGTH,
        "PETREPORT_CONTACT_NAME_LENGTH": PETREPORT_CONTACT_NAME_LENGTH,
        "PETREPORT_CONTACT_NUMBER_LENGTH": PETREPORT_CONTACT_NUMBER_LENGTH,
        "PETREPORT_CONTACT_EMAIL_LENGTH": PETREPORT_CONTACT_EMAIL_LENGTH,
        "PETREPORT_CONTACT_LINK_LENGTH": PETREPORT_CONTACT_LINK_LENGTH 
    }, RequestContext(request))

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

        payload = json.dumps({"breeds":breeds})
        return HttpResponse(payload, mimetype="application/json")

    else:
        raise Http404

    
#AJAX Request to bookmark a PetReport
@login_required
def bookmark(request):
    if request.method == "POST" and request.is_ajax() == True:
        profile = request.user.userprofile
        petreport_id = request.POST['petreport_id']
        petreport = get_object_or_404(PetReport, pk=petreport_id)
        action = request.POST['action']
        print_debug_msg("User: %s, Action: %s, petreport: %s" % (profile.user.username, action, petreport))

        #If the user has bookmarked this pet and the action is to remove it...
        if ((petreport.UserProfile_has_bookmarked(profile) == True) and (action == "Remove Bookmark")) :
            petreport.bookmarked_by.remove(profile)
            petreport.save()
            message = "You have successfully removed the bookmark for this pet." 
            text = "Bookmark this Pet"

            print_debug_msg("REMOVING BOOKMARK")

            # Log removing the PetReport bookmark for this UserProfile
            Activity.log_activity("ACTIVITY_PETREPORT_REMOVE_BOOKMARK", profile, source=petreport)

        #If the user has NOT bookmarked this pet and the action is to bookmark it...
        elif ((petreport.UserProfile_has_bookmarked(profile) == False) and (action == "Bookmark this Pet")):
            petreport.bookmarked_by.add(profile)
            petreport.save()
            print_info_msg ('Bookmarked pet report %s for %s' % (petreport, profile))
            message = "You have successfully bookmarked this pet!" 
            text = "Remove Bookmark"

            print_debug_msg("ADDING BOOKMARK")

            # Log adding the PetReport bookmark for this UserProfile
            Activity.log_activity("ACTIVITY_PETREPORT_ADD_BOOKMARK", profile, source=petreport)

        else:
            print_info_msg ("User has bookmarked the pet: " + str(petreport.UserProfile_has_bookmarked(profile)))
            message = "Unable to "+ action + "!"
            text = action
        payload = json.dumps ({"message":message, "text":text})
        return HttpResponse(payload, mimetype="application/json")
    else:
        raise Http404


