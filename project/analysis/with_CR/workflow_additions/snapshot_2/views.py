from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import *
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import JsonResponse
from django.http import Http404
from django.contrib import messages
from matching.views import *
from django.conf import settings
from django.contrib.sites.models import Site
from home.models import Activity
from socializing.models import UserProfile
from reporting.models import PetReport, PetReportForm
from matching.models import PetMatch
from utilities.utils import *
from constants import *
from home.constants import *
from verifying.models import PetReunion, PetReunionForm
from verifying.constants import *
from reporting.decorators import *
from crowdwork import EPMCrowdRouter
import datetime, re, time, json, ipdb, project.settings

@login_required
def mixed(request):
    response = EPMCrowdRouter().pipeline("MixedWorkFlow", request)
    if response.method == "GET":
        return render_to_response(response.response["path"], response.response, RequestContext(request))
    else:
        messages.success(request, "Thank you for helping!")
        return redirect(response.response["path"])

def get(request, petreport_id):
    pet_report = get_object_or_404(PetReport, pk = petreport_id)
    user_has_bookmarked = False

    if pet_report.status == 'Lost':
        matches = PetMatch.objects.all().filter(lost_pet = pet_report)
    else:
        matches = PetMatch.objects.all().filter(found_pet = pet_report)

    num_workers = len(pet_report.workers.all())
    if request.user.is_authenticated() == True:
        user_is_worker = pet_report.UserProfile_is_worker(request.user.userprofile)
    else:
        user_is_worker = False

    if UserProfile.get_UserProfile(username=request.user.username) and (pet_report.proposed_by == request.user.userprofile) and not pet_report.closed:
        edit_petreport = True
    else:
        edit_petreport = False

    if request.user.is_authenticated() == True:
        userprofile = request.user.userprofile
        if pet_report.UserProfile_has_bookmarked(userprofile) == True:
            user_has_bookmarked = True

    #Fetch PetReunion object if it exists.
    pet_reunion = pet_report.get_PetReunion()

    return render_to_response(HTML_PRDP, {
        'pet_report': pet_report,
        'pet_reunion': pet_reunion,
        'petreport_fields': pet_report.get_display_fields(),
        'edit_petreport': edit_petreport,
        'site_domain': Site.objects.get_current().domain,
        'num_workers':num_workers,
        'user_is_worker':user_is_worker,
        'matches': matches,
        'user_has_bookmarked':user_has_bookmarked
    }, RequestContext(request))

#Given a PetReport ID, just return the PetReport JSON.
def get_PetReport_JSON(request):
    if (request.method == "GET") and (request.is_ajax() == True):
        petreport = get_object_or_404(PetReport, pk=int(request.GET["petreport_id"]))
        return JsonResponse({"petreport":petreport.to_DICT()}, safe=False)
    else:
        raise Http404

#Given a Page Number, return a list of PetReports.
def get_PetReports_JSON(request):
    if request.is_ajax() == True:
        filters = dict(request.GET)
        filters["closed"] = False
        #Grab Pets by Filter Options.
        results = PetReport.filter(filters, page=request.GET["page"], limit=NUM_PETREPORTS_HOMEPAGE)
        pet_reports = [{
            "ID"                    : pr.id,
            "proposed_by_username"  : pr.proposed_by.user.username,
            "pet_name"              : pr.pet_name,
            "pet_type"              : pr.pet_type,
            "status"                : pr.status,
            "img_path"              : pr.thumb_path.name
        } for pr in results["petreports"]]

        return JsonResponse({"pet_reports_list":pet_reports, "count":len(pet_reports), "total_count": results["count"]}, safe=False)
    else:
        raise Http404

@login_required
def new(request):
    return render_to_response(HTML_PETREPORT_FORM, {
        "status": "ok",
        "path": HTML_PETREPORT_FORM,
        "form": PetReportForm(), #Unbound Form
        "RECAPTCHA_CLIENT_SECRET": settings.RECAPTCHA_CLIENT_SECRET,
        "PETREPORT_TAG_INFO_LENGTH":PETREPORT_TAG_INFO_LENGTH,
        "PETREPORT_DESCRIPTION_LENGTH":PETREPORT_DESCRIPTION_LENGTH,
        "PETREPORT_CONTACT_NAME_LENGTH": PETREPORT_CONTACT_NAME_LENGTH,
        "PETREPORT_CONTACT_NUMBER_LENGTH": PETREPORT_CONTACT_NUMBER_LENGTH,
        "PETREPORT_CONTACT_EMAIL_LENGTH": PETREPORT_CONTACT_EMAIL_LENGTH,
        "PETREPORT_CONTACT_LINK_LENGTH": PETREPORT_CONTACT_LINK_LENGTH
    }, RequestContext(request))

@login_required
def submit(request):
    form = PetReportForm(request.POST, request.FILES)
    if not request.POST["g-recaptcha-response"]:
        messages.error (request, "Please fill in the RECAPTCHA.")
        return redirect(URL_PETREPORT_FORM)

    if not recaptcha_ok(request.POST["g-recaptcha-response"]):
        messages.error(request, "CAPTCHA was not correct. Please try again.")
        return redirect(URL_PETREPORT_FORM)

    #Let's make some adjustments to non-textual form fields before converting to a PetReportForm.
    geo_lat = request.POST ["geo_location_lat"] or ""
    geo_long = request.POST ["geo_location_long"] or ""

    if (geo_lat == "" or geo_lat == "None") or (geo_long == "" or geo_long == "None"):
        request.POST ['geo_location_lat'] = 0.00
        request.POST ['geo_location_long'] = 0.00
    else:
        request.POST ["geo_location_lat"] = float("%.5f" % float(geo_lat))
        request.POST ["geo_location_long"] = float("%.5f" % float(geo_long))

    if form.is_valid() == True:
        #Create (but do not save) the Pet Report Object associated with this form data.
        pr = form.save(commit=False)
        pr.proposed_by = request.user.userprofile

        #Deal with Contact Information.
        if pr.contact_name.strip() == "":
            pr.contact_name = None
        if pr.contact_email.strip() == "":
            pr.contact_email = None
        if pr.contact_number.strip() == "":
            pr.contact_number = None
        if pr.contact_link.strip() == "":
            pr.contact_link = None

        pr.breed = pr.breed.strip()
        print_info_msg ("Pet Report Image Path: %s" % pr.img_path)

        #Make and save images from img_path and thumb_path AND save the PetReport.
        pr.set_images(pr.img_path, save=True, rotation=request.POST.get("img_rotation"))

        #Add reputation points for submitting a pet report
        request.user.userprofile.update_reputation("ACTIVITY_PETREPORT_SUBMITTED")
        message = "Thank you for your submission. %s %s (%s) is front row on the gallery! " % (pr.status, pr.pet_type, pr.pet_name)
        if pr.status == 'Lost':
            messages.success (request, message + "Your contribution will go a long way towards helping volunteers find your lost pet.")
        else:
            messages.success (request, message + "Your contribution will go a long way towards helping volunteers match your found pet.")

        #Log the PetReport submission for this UserProfile
        Activity.log_activity("ACTIVITY_PETREPORT_SUBMITTED", request.user.userprofile, source=pr)
        print_success_msg("Pet Report submitted successfully")

        #Check to see if there are any matching petreports that have the same microchip ID.
        matching_pet = pr.find_by_microchip_id()
        if matching_pet != None: #Send an email about the match!
            contact1 = generate_pet_contacts(pr)[0]
            contact2 = generate_pet_contacts(matching_pet)[0]
            email_body = render_to_string(EMAIL_BODY_MATCH_BY_MICROCHIP_ID, {
                "pet": pr,
                "other_pet": matching_pet,
                "site": Site.objects.get_current()
            })
            send_email(EMAIL_SUBJECT_MATCH_BY_MICROCHIP_ID, email_body, None, [contact1["email"]])
        return redirect(URL_HOME)
    else:
        messages.error(request, "Something went wrong. Please check the fields and try again.")
        print_error_msg ("Pet Report not submitted successfully")
        print_error_msg (form.errors)
        print_error_msg (form.non_field_errors())
        return render_to_response(HTML_PETREPORT_FORM, {
            "form": form,
            "PETREPORT_TAG_INFO_LENGTH":PETREPORT_TAG_INFO_LENGTH,
            "PETREPORT_DESCRIPTION_LENGTH":PETREPORT_DESCRIPTION_LENGTH,
            "PETREPORT_CONTACT_NAME_LENGTH": PETREPORT_CONTACT_NAME_LENGTH,
            "PETREPORT_CONTACT_NUMBER_LENGTH": PETREPORT_CONTACT_NUMBER_LENGTH,
            "PETREPORT_CONTACT_EMAIL_LENGTH": PETREPORT_CONTACT_EMAIL_LENGTH,
            "PETREPORT_CONTACT_LINK_LENGTH": PETREPORT_CONTACT_LINK_LENGTH
        }, RequestContext(request))

@login_required
@allow_only_proposer
@allow_only_before_close
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
            return redirect(URL_PRDP + "%d/" % pet_report.id)
        form = PetReportForm(instance=pet_report)
        messages.error(request, "Something went wrong. Please check the fields and try again.")
    else:
        raise Http404

    return render_to_response(HTML_EDIT_PETREPORT, {
        "form": form,
        "petreport": pet_report,
        "RECAPTCHA_CLIENT_SECRET": settings.RECAPTCHA_CLIENT_SECRET,
        "PETREPORT_TAG_INFO_LENGTH":PETREPORT_TAG_INFO_LENGTH,
        "PETREPORT_DESCRIPTION_LENGTH":PETREPORT_DESCRIPTION_LENGTH,
        "PETREPORT_CONTACT_NAME_LENGTH": PETREPORT_CONTACT_NAME_LENGTH,
        "PETREPORT_CONTACT_NUMBER_LENGTH": PETREPORT_CONTACT_NUMBER_LENGTH,
        "PETREPORT_CONTACT_EMAIL_LENGTH": PETREPORT_CONTACT_EMAIL_LENGTH,
        "PETREPORT_CONTACT_LINK_LENGTH": PETREPORT_CONTACT_LINK_LENGTH
    }, RequestContext(request))

@login_required
@allow_only_proposer
@allow_only_one_close
def close(request, petreport_id):
    petreport = get_object_or_404(PetReport, pk=petreport_id)
    if request.user.userprofile.id == petreport.proposed_by.id:
        if request.method == "POST":
            if not request.POST.get("g-recaptcha-response"):
                messages.error(request, "Please fill in the RECAPTCHA.")
                return redirect(request.path)

            if not recaptcha_ok(request.POST["g-recaptcha-response"]):
                messages.error(request, "RECAPTCHA was not correct. Please try again.")
                return redirect(request.path)

            form = PetReunionForm(request.POST, request.FILES)
            if form.is_valid() == True:
                petreunion = form.save(commit=False)
                petreunion.petreport = petreport

                #If this pet was matched with another one, then link the matched pet into the new PetReunion object.
                if petreport.has_been_successfully_matched() == True:
                    matched_petreport = petreport.get_matched_PetReport()
                    petreunion.matched_petreport = matched_petreport

                petreunion.set_images(petreunion.img_path, save=True, rotation=request.POST.get("img_rotation")) #This saves the PetReunion.
                messages.success(request, "You've successfully closed this Pet Report. Thank you for helping reunite this pet!")
                print_success_msg("Pet Report closed successfully.")
                return redirect(URL_HOME)
            else:
                messages.error(request, "Something went wrong. Please check the fields and try again.")
                print_error_msg ("Pet Reunion not submitted successfully")
        else:
            form = PetReunionForm()

        return render_to_response(HTML_PETREUNION_FORM, {
            'form':form,
            'petreport':petreport,
            "RECAPTCHA_CLIENT_SECRET": settings.RECAPTCHA_CLIENT_SECRET,
            "PETREUNION_DESCRIPTION_LENGTH": PETREUNION_DESCRIPTION_LENGTH,
            "PETREUNION_REASON_LENGTH": PETREUNION_REASON_LENGTH
        }, RequestContext(request))
    else:
        raise Http404

def get_pet_breeds(request):
    if request.is_ajax() == True:
        pet_type = request.GET["pet_type"]
        pet_types = {
            "Dog": PETREPORT_PET_TYPE_DOG,
            "Cat": PETREPORT_PET_TYPE_CAT,
            "Horse": PETREPORT_PET_TYPE_HORSE,
            "Bird": PETREPORT_PET_TYPE_BIRD,
            "Rabbit": PETREPORT_PET_TYPE_RABBIT,
            "Turtle": PETREPORT_PET_TYPE_TURTLE,
            "Snake": PETREPORT_PET_TYPE_SNAKE,
            "Other": PETREPORT_PET_TYPE_OTHER
        }
        breeds = PetReport.get_pet_breeds(pet_types[pet_type])
        breeds = [{"id": breed, "text":breed} for index, breed in enumerate(breeds)]
        return JsonResponse({"breeds":breeds}, safe=False)
    else:
        raise Http404

def get_event_tags(request):
    if request.is_ajax() == True:
        event_tags = [{"id": event_tag, "text":event_tag} for event_tag in PetReport.get_event_tags()]
        return JsonResponse({"event_tags":event_tags}, safe=False)
    else:
        raise Http404

@login_required
def bookmark(request):
    if request.method == "POST" and request.is_ajax() == True:
        profile = request.user.userprofile
        petreport = get_object_or_404(PetReport, pk=request.POST['petreport_id'])
        action = request.POST['action']

        if ((petreport.UserProfile_has_bookmarked(profile) == True) and (action == "Remove Bookmark")) :
            petreport.bookmarked_by.remove(profile)
            petreport.save()
            message = "You have successfully removed the bookmark for this pet."
            text = "Bookmark this Pet"
            Activity.log_activity("ACTIVITY_PETREPORT_REMOVE_BOOKMARK", profile, source=petreport)

        elif ((petreport.UserProfile_has_bookmarked(profile) == False) and (action == "Bookmark this Pet")):
            petreport.bookmarked_by.add(profile)
            petreport.save()
            message = "You have successfully bookmarked this pet!"
            text = "Remove Bookmark"
            Activity.log_activity("ACTIVITY_PETREPORT_ADD_BOOKMARK", profile, source=petreport)
        else:
            raise Http404
        return JsonResponse({"message":message, "text":text}, safe=False)
    else:
        raise Http404
