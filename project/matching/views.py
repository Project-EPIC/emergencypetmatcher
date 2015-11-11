from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import models, IntegrityError
from django.db.models import Min
from django.contrib import messages
from django.contrib.messages.api import get_messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import *
from django.core import mail
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
from random import choice, uniform
from pprint import pprint
from home.models import Activity
from reporting.models import PetReport
from matching.models import PetMatch
from verifying.models import PetMatchCheck
from utilities.utils import *
from constants import *
from home.constants import *
from matching.decorators import *
import datetime, re, json, pdb, urllib, urllib2, ssl

#Display the PetMatch object
def get(request, petmatch_id):
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

#Given a PetMatch ID, just return the PetMatch JSON.
def get_PetMatch_JSON(request, petmatch_id):
    if (request.method == "GET") and (request.is_ajax() == True):
        petmatch = get_object_or_404(PetMatch, pk=petmatch_id)
        return JsonResponse({"petmatch":petmatch.to_DICT()}, safe=False)
    else:
        raise Http404

def get_PetMatches_JSON(request):
    if request.is_ajax() == True:
        filters = dict(request.GET)
        filters['has_failed'] = False
        #Grab Pet Matches by Filter Options.
        results = PetMatch.filter(filters, page=request.GET["page"], limit=NUM_PETMATCHES_HOMEPAGE)
        pet_matches = [{
            "ID"                    : pm.id,
            "proposed_by_username"  : pm.proposed_by.user.username,
            "lost_pet_name"         : pm.lost_pet.pet_name,
            "found_pet_name"        : pm.found_pet.pet_name,
            "lost_pet_img_path"     : pm.lost_pet.thumb_path.name,
            "found_pet_img_path"    : pm.found_pet.thumb_path.name
        } for pm in results["petmatches"]]

        return JsonResponse({"pet_matches_list":pet_matches, "count":len(pet_matches), "total_count": results["count"]}, safe=False)
    else:
        raise Http404

@login_required
@allow_only_before_closing
def vote(request, petmatch_id):
    if request.method == "POST":
        userprofile = request.user.userprofile
        vote = request.POST ['vote']
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

        return JsonResponse({
            "vote":vote,
            "message":message,
            "threshold_reached": threshold_reached,
            "num_downvotes":num_downvotes,
            "num_upvotes":num_upvotes
        }, safe=False)

    else:
        raise Http404

@login_required
def get_candidate_PetReports(request):
    if request.method == "GET" and request.is_ajax() == True:
        petreport_id = int(request.GET["target_petreport_id"])
        page = int(request.GET["page"])
        if page < 1:
            page = 1
        petreport = get_object_or_404(PetReport, pk=petreport_id)
        candidates = petreport.get_candidate_PetReports()
        candidates_count = len(candidates) #Get the candidate count for pagination purposes.
        paged_candidates = petreport.get_ranked_candidate_PetReports(candidates=candidates, page=page)
        paged_candidates = [{
            "ID": pr.id,
            "status":pr.status,
            "proposed_by_username": pr.proposed_by.user.username,
            "pet_name": pr.pet_name,
            "pet_type": pr.pet_type,
            "img_path": pr.img_path.name
        } for pr in paged_candidates]

        return JsonResponse({
            "pet_reports_list":paged_candidates,
            "count":len(paged_candidates),
            "total_count": candidates_count
        }, safe=False)
    else:
        raise Http404

@login_required
@disallow_closed_petreports
def match(request, petreport_id):
    if request.method == "GET":
        target_petreport = get_object_or_404(PetReport, pk=petreport_id)
        #Are there any candidates?
        candidates_count = len(target_petreport.get_candidate_PetReports())
        #Add the UserProfile to the PetReport's workers list.
        target_petreport.workers.add(request.user.userprofile)

        if candidates_count == 0:
            messages.info (request, "Sorry, there are no pet reports for the selected pet report to match. However, you have been added as a worker for this pet.")
            return redirect(URL_HOME)

        return render_to_response (HTML_MATCHING, {
            'target_petreport': target_petreport,
            'petreport_fields': target_petreport.get_display_fields(),
            "candidates_count":candidates_count
        }, RequestContext(request))
    else:
        raise Http404

@login_required
@disallow_closed_petreports
@disallow_incompatible_petreports
def propose(request, target_id, candidate_id):
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
                    return redirect(URL_MATCHING + target_id + "/")

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
                    return redirect(URL_MATCHING + target_id + "/")

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
        return redirect(URL_HOME)

    else:
        if request.method == "POST" and not request.POST["g-recaptcha-response"]:
            messages.error(request, "Please Fill in the RECAPTCHA.")

        if (target.pet_type != candidate.pet_type) or (target.status == candidate.status):
            messages.error(request, "This proposal is invalid! Please try another one.")
            return redirect(URL_MATCHING + str(target.id))

        return render_to_response(HTML_PROPOSE_MATCH, {
            'RECAPTCHA_CLIENT_SECRET': settings.RECAPTCHA_CLIENT_SECRET,
            'target': target,
            'candidate': candidate,
            'petreport_fields': [{'attr':a['attr'], 'label':a['label'], 'lost_pet_value':a['value'], 'found_pet_value':b['value']} for a,b in zip(target.get_display_fields(), candidate.get_display_fields())]
        }, RequestContext(request))
