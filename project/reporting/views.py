from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import *
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.http import JsonResponse
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
from django.template.loader import render_to_string
from pprint import pprint
from PIL import Image
from utilities.utils import *
from constants import *
from home.constants import *
from verifying.models import PetReunion, PetReunionForm
from verifying.constants import *
from reporting.decorators import *
import datetime, re, time, json, ipdb, project.settings

def mixed0(request):
    petmatch_id = PetMatch.objects.filter(has_failed=False, lost_pet__closed=False, found_pet__closed=False).order_by("?").first().id
    return redirect("/reporting/mixed1/%s" % petmatch_id)

def mixed1(request, petmatch_id):
    if request.method == "POST":
        userprofile = request.user.userprofile
        if request.POST.get("up") != None:
            vote = "upvote"
        else:
            vote = "downvote"
        pm = get_object_or_404(PetMatch, pk=petmatch_id)

        if vote == "upvote":
            if pm.UserProfile_has_voted(userprofile) is False: # If the user is voting for the 1st time, add reputation points
                userprofile.update_reputation("ACTIVITY_PETMATCH_UPVOTE")

            pm.up_votes.add(userprofile)
            pm.down_votes.remove(userprofile)
            Activity.log_activity("ACTIVITY_PETMATCH_UPVOTE", userprofile, source=pm)
            message = "You have upvoted this PetMatch!"

        elif vote == "downvote":
            if pm.UserProfile_has_voted(userprofile) is False: # If the user is voting for the 1st time, add reputation points
                userprofile.update_reputation("ACTIVITY_PETMATCH_DOWNVOTE")

            pm.down_votes.add(userprofile)
            pm.up_votes.remove(userprofile)
            Activity.log_activity("ACTIVITY_PETMATCH_DOWNVOTE", userprofile, source=pm)
            message = "You have downvoted this PetMatch!"

        #Was the petmatch triggered for verification? Check here.
        threshold_reached = pm.has_reached_threshold()

        #If the votes reach the threshold, prepare for pet checking!
        if threshold_reached == True:
            new_check = PetMatchCheck.objects.create(petmatch=pm)
            Activity.log_activity("ACTIVITY_PETMATCHCHECK_VERIFY", userprofile, source=new_check)
            message = new_check.send_messages_to_contacts()

        num_upvotes = len(pm.up_votes.all())
        num_downvotes = len(pm.down_votes.all())
        petreport_id = PetReport.objects.filter(closed=False).order_by("?").first().id
        return redirect("/reporting/mixed2/%s" % petreport_id)

    else:
        pm = get_object_or_404(PetMatch, pk=petmatch_id)
        voters = list(pm.up_votes.all()) + list(pm.down_votes.all())

        #Need to check if the user is authenticated (non-anonymous) to find out if he/she has voted on this PetMatch.
        if request.user.is_authenticated() == True:
            user_has_voted = pm.UserProfile_has_voted(request.user.userprofile)
        else:
            user_has_voted = False

        num_upvotes = len(pm.up_votes.all())
        num_downvotes = len(pm.down_votes.all())

        ctx = {
            "petmatch": pm,
            "action": "/reporting/mixed1/" + str(pm.id) + "/",
            "site_domain":Site.objects.get_current().domain,
            "petreport_fields": pm.get_display_fields(),
            "num_voters": len(voters),
            "user_has_voted": user_has_voted,
            "num_upvotes":num_upvotes,
            "num_downvotes":num_downvotes
        }

        if pm.lost_pet.closed:
            ctx["petreunion"] = pm.lost_pet.get_PetReunion()
        elif pm.found_pet.closed:
            ctx["petreunion"] = pm.found_pet.get_PetReunion()
        return render_to_response(HTML_PMDP, ctx, RequestContext(request))

def mixed2(request, petreport_id):
    if request.method == "POST":
        import ipdb; ipdb.set_trace()
        target = get_object_or_404(PetReport, pk=petreport_id)
        candidate = get_object_or_404(PetReport, pk=request.POST["candidate_id"])
        return redirect('/reporting/mixed3/%s/%s/' % (target.id, candidate.id))
    else:
        target_petreport = get_object_or_404(PetReport, pk=petreport_id)
        #Are there any candidates?
        candidates_count = len(target_petreport.get_candidate_PetReports())
        #Add the UserProfile to the PetReport's workers list.
        target_petreport.workers.add(request.user.userprofile)

        if candidates_count == 0:
            messages.info (request, "Sorry, there are no pet reports for the selected pet report to match. However, you have been added as a worker for this pet.")
            return redirect(URL_HOME)

        return render_to_response (HTML_MATCHING, {
            'action': '/reporting/mixed2/%s/' % petreport_id,
            'target_petreport': target_petreport,
            'petreport_fields': target_petreport.get_display_fields(),
            "candidates_count":candidates_count
        }, RequestContext(request))

def mixed3(request, target_id, candidate_id):
    import ipdb; ipdb.set_trace()
    target = get_object_or_404(PetReport, pk=target_id)
    candidate = get_object_or_404(PetReport, pk=candidate_id)

    if request.method == "POST" and request.POST.get("g-recaptcha-response"):
        if not recaptcha_ok(request.POST["g-recaptcha-response"]):
            messages.error(request, "CAPTCHA was not correct. Please try again.")
            return redirect(request.path)
        proposed_by = request.user.userprofile

        if target.status == "Lost":
            pm = PetMatch(lost_pet=target, found_pet=candidate, proposed_by=proposed_by)
        else:
            pm = PetMatch(lost_pet=candidate, found_pet=target, proposed_by=proposed_by)

        #Try saving the PetMatch object.
        # We will expect the following output:
        # None --> PetMatch was not inserted properly OR DUPLICATE PETMATCH
        # PetMatch Object --> Existing PetMatch (UPDATE) OR Brand new PetMatch.
        # "Existing" means the PetMatch to be saved is the same PetMatch found, "Duplicate" means
        # another PetMatch with the same Lost+Found Pets were found.
        (result, outcome) = pm.save()

        if result != None:
            if outcome == PETMATCH_OUTCOME_UPDATE:
                #Has the user voted for this PetMatch before?
                user_has_voted = result.UserProfile_has_voted(proposed_by)

                if user_has_voted == UPVOTE or user_has_voted == DOWNVOTE:
                    messages.error(request, "This Pet Match has already been proposed, and you have voted for it already!")
                    return redirect("/reporting/mixed2/%s/" % (target.id))

                # add voting reputation points if the user didn't vote before for this duplicate petmatch
                # if (proposed_by not in result.up_votes.all()) and (proposed_by not in result.down_votes.all()):
                if pm.UserProfile_has_voted(userprofile) is False:
                    proposed_by.update_reputation("ACTIVITY_PETMATCH_UPVOTE")

                result.up_votes.add(proposed_by)
                result.save()
                messages.success(request, "Because there was an existing match between the two pet reports that you tried to match, You have successfully up-voted the existing pet match. Help spread the word about this match!")
                Activity.log_activity("ACTIVITY_PETMATCH_UPVOTE", proposed_by, source=result)

            elif outcome == PETMATCH_OUTCOME_NEW_PETMATCH:
                messages.success(request, "Congratulations, the pet match was successful! You can view your pet match in the home page and in your profile. Help spread the word about your match!")
                Activity.log_activity("ACTIVITY_PETMATCH_PROPOSED", proposed_by, source=result)
                # add reputation points for proposing a new petmatch
                proposed_by.update_reputation("ACTIVITY_PETMATCH_PROPOSED")

        else:
            if outcome == PETMATCH_OUTCOME_DUPLICATE_PETMATCH:
                result = PetMatch.get_PetMatch(target, candidate)
                #Has the user voted for this PetMatch before?
                user_has_voted = result.UserProfile_has_voted(proposed_by)

                if user_has_voted == UPVOTE or user_has_voted == DOWNVOTE:
                    messages.error(request, "This Pet Match has already been proposed, and you have voted for it already!")
                    return redirect("/reporting/mixed2/%s/" % (target.id))

                # add voting reputation points if the user didn't vote before for this duplicate petmatch
                if user_has_voted == False:
                    proposed_by.update_reputation("ACTIVITY_PETMATCH_UPVOTE")

                result.up_votes.add(proposed_by)
                result.save()
                messages.success(request, "Because there was an existing match between the two pet reports that you tried to match, You have successfully up-voted the existing pet match. Help spread the word about this match!")
                Activity.log_activity("ACTIVITY_PETMATCH_UPVOTE", proposed_by, source=result)
            else:
                messages.error(request, "A Problem was found when trying to propose the PetMatch. We have been notified of the issue and will fix it as soon as possible.")

        #Finally, return the redirect.
        return redirect("/reporting/mixed4/%s/" % pm.id)

    else:
        if request.method == "POST" and not request.POST["g-recaptcha-response"]:
            messages.error(request, "Please Fill in the RECAPTCHA.")

        if (target.pet_type != candidate.pet_type) or (target.status == candidate.status):
            messages.error(request, "This proposal is invalid! Please try another one.")
            return redirect("/reporting/mixed2/%s/" % (target.id))

        return render_to_response(HTML_PROPOSE_MATCH, {
            'RECAPTCHA_CLIENT_SECRET': settings.RECAPTCHA_CLIENT_SECRET,
            'action': '/reporting/mixed3/%s/%s/' % (target_id, candidate_id),
            'target': target,
            'candidate': candidate,
            'petreport_fields': [{'attr':a['attr'], 'label':a['label'], 'lost_pet_value':a['value'], 'found_pet_value':b['value']} for a,b in zip(target.get_display_fields(), candidate.get_display_fields())]
        }, RequestContext(request))

def mixed4(request, petmatch_id):
    if request.method == "POST":
        userprofile = request.user.userprofile
        if request.POST.get("up") != None:
            vote = "upvote"
        else:
            vote = "downvote"
        pm = get_object_or_404(PetMatch, pk=petmatch_id)

        if vote == "upvote":
            if pm.UserProfile_has_voted(userprofile) is False: # If the user is voting for the 1st time, add reputation points
                userprofile.update_reputation("ACTIVITY_PETMATCH_UPVOTE")

            pm.up_votes.add(userprofile)
            pm.down_votes.remove(userprofile)
            Activity.log_activity("ACTIVITY_PETMATCH_UPVOTE", userprofile, source=pm)
            message = "You have upvoted this PetMatch!"

        elif vote == "downvote":
            if pm.UserProfile_has_voted(userprofile) is False: # If the user is voting for the 1st time, add reputation points
                userprofile.update_reputation("ACTIVITY_PETMATCH_DOWNVOTE")

            pm.down_votes.add(userprofile)
            pm.up_votes.remove(userprofile)
            Activity.log_activity("ACTIVITY_PETMATCH_DOWNVOTE", userprofile, source=pm)
            message = "You have downvoted this PetMatch!"

        #Was the petmatch triggered for verification? Check here.
        threshold_reached = pm.has_reached_threshold()

        #If the votes reach the threshold, prepare for pet checking!
        if threshold_reached == True:
            new_check = PetMatchCheck.objects.create(petmatch=pm)
            Activity.log_activity("ACTIVITY_PETMATCHCHECK_VERIFY", userprofile, source=new_check)
            message = new_check.send_messages_to_contacts()

        num_upvotes = len(pm.up_votes.all())
        num_downvotes = len(pm.down_votes.all())
        messages.success(request, "Thank you for helping out!")
        return redirect(URL_HOME)

    else:
        pm = get_object_or_404(PetMatch, pk=petmatch_id)
        voters = list(pm.up_votes.all()) + list(pm.down_votes.all())

        #Need to check if the user is authenticated (non-anonymous) to find out if he/she has voted on this PetMatch.
        if request.user.is_authenticated() == True:
            user_has_voted = pm.UserProfile_has_voted(request.user.userprofile)
        else:
            user_has_voted = False

        num_upvotes = len(pm.up_votes.all())
        num_downvotes = len(pm.down_votes.all())

        ctx = {
            "petmatch": pm,
            "action": "/reporting/mixed4/" + str(pm.id) + "/",
            "site_domain":Site.objects.get_current().domain,
            "petreport_fields": pm.get_display_fields(),
            "num_voters": len(voters),
            "user_has_voted": user_has_voted,
            "num_upvotes":num_upvotes,
            "num_downvotes":num_downvotes
        }

        if pm.lost_pet.closed:
            ctx["petreunion"] = pm.lost_pet.get_PetReunion()
        elif pm.found_pet.closed:
            ctx["petreunion"] = pm.found_pet.get_PetReunion()
        return render_to_response(HTML_PMDP, ctx, RequestContext(request))


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
def submit(request):
    if request.method == "POST" and request.POST["g-recaptcha-response"]:
        if not recaptcha_ok(request.POST["g-recaptcha-response"]):
            messages.error(request, "CAPTCHA was not correct. Please try again.")
            return redirect(request.path)

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
                'form':form,
                "PETREPORT_TAG_INFO_LENGTH":PETREPORT_TAG_INFO_LENGTH,
                "PETREPORT_DESCRIPTION_LENGTH":PETREPORT_DESCRIPTION_LENGTH,
                "PETREPORT_CONTACT_NAME_LENGTH": PETREPORT_CONTACT_NAME_LENGTH,
                "PETREPORT_CONTACT_NUMBER_LENGTH": PETREPORT_CONTACT_NUMBER_LENGTH,
                "PETREPORT_CONTACT_EMAIL_LENGTH": PETREPORT_CONTACT_EMAIL_LENGTH,
                "PETREPORT_CONTACT_LINK_LENGTH": PETREPORT_CONTACT_LINK_LENGTH
            }, RequestContext(request))
    else:
        if request.method == "POST" and not request.POST["g-recaptcha-response"]:
            messages.error (request, "Please fill in the RECAPTCHA.")
        form = PetReportForm() #Unbound Form

    return render_to_response(HTML_PETREPORT_FORM, {
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
