from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
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
from verifying.models import PetCheck
from utilities.utils import *
from constants import *
from home.constants import *
import datetime, re, json, pdb, urllib, urllib2

#Display the PetMatch object
def get_PetMatch(request, petmatch_id):
    pm = get_object_or_404(PetMatch, pk=petmatch_id)
    voters = list(pm.up_votes.all()) + list(pm.down_votes.all())

    #Need to check if the user is authenticated (non-anonymous) to find out if he/she has voted on this PetMatch.
    if request.user.is_authenticated() == True:
        user_has_voted = pm.UserProfile_has_voted(request.user.userprofile)
    else:
        user_has_voted = False

    num_upvotes = len(pm.up_votes.all())
    num_downvotes = len(pm.down_votes.all())

    if pm.is_successful == True:
        messages.success(request, "These pet reports have been matched! Thank you digital volunteers!")
    elif pm.has_failed == True:
        messages.info(request, "Sorry, this match did not succeed in reuniting pet and pet owner.")
    elif pm.is_being_checked() == True:
        messages.info(request, "These pet reports are currently being checked by their owners! Votes are closed.")

    fields = pm.pack_PetReport_fields()

    if request.is_ajax() == True:
        html = HTML_PMDP
    else:
        html = HTML_PMDP_FULL    

    return render_to_response(html, {  "petmatch": pm,
                                        "site_domain":Site.objects.get_current().domain,
                                        "pet_fields": fields,
                                        "num_voters": len(voters), 
                                        "user_has_voted": user_has_voted, 
                                        "num_upvotes":num_upvotes, 
                                        "num_downvotes":num_downvotes}, RequestContext(request))  

#Vote on the PetMatch    
@login_required
def vote(request):
    if request.method == "POST":
        userprofile = request.user.userprofile
        vote = request.POST ['vote']
        pm = get_object_or_404(PetMatch, pk=request.POST["match_id"])

        print_info_msg ("VOTE: %s" % vote)
        print_info_msg ("#UPVOTES: %d" % len(pm.up_votes.all()))
        print_info_msg ("#DOWNVOTES: %d" % len(pm.down_votes.all()))

        if vote == "upvote":
            # If the user is voting for the 1st time, add reputation points
            if pm.UserProfile_has_voted(userprofile) is False:
                userprofile.update_reputation("ACTIVITY_PETMATCH_UPVOTE")
            
            pm.up_votes.add(userprofile)
            pm.down_votes.remove(userprofile)

            Activity.log_activity("ACTIVITY_PETMATCH_UPVOTE", userprofile, source=pm)
            message = "You have upvoted this PetMatch and earned %d Pet Points!" % (ACTIVITIES["ACTIVITY_PETMATCH_UPVOTE"]["reward"])

        elif vote == "downvote":
            # If the user is voting for the 1st time, add reputation points
            if pm.UserProfile_has_voted(userprofile) is False:
                userprofile.update_reputation("ACTIVITY_PETMATCH_DOWNVOTE")
                
            pm.down_votes.add(userprofile)
            pm.up_votes.remove(userprofile)
            Activity.log_activity("ACTIVITY_PETMATCH_DOWNVOTE", userprofile, source=pm)
            message = "You have downvoted this PetMatch and earned %d Pet Points!" % (ACTIVITIES["ACTIVITY_PETMATCH_DOWNVOTE"]["reward"])

        #Was the petmatch triggered for verification? Check here.
        threshold_reached = pm.has_reached_threshold() 
        
        #If the votes reach the threshold, prepare for pet checking!
        if threshold_reached == True:
            new_check = PetCheck.objects.create(petmatch=pm)
            Activity.log_activity("ACTIVITY_PETCHECK_VERIFY", userprofile, source=new_check)
            message = new_check.verify_PetMatch()
            
        num_upvotes = len(pm.up_votes.all())
        num_downvotes = len(pm.down_votes.all())
        payload = json.dumps ({ "vote":vote, 
                                "message":message, 
                                "threshold_reached": threshold_reached, 
                                "num_downvotes":num_downvotes, 
                                "num_upvotes":num_upvotes })
        return HttpResponse(payload, mimetype="application/json")

    else:
        raise Http404


@login_required
def get_candidate_PetReports(request):
    if request.method == "GET" and request.is_ajax() == True:
        petreport_id = int(request.GET["target_petreport_id"])
        page = int(request.GET["page"])
        petreport = get_object_or_404(PetReport, pk=petreport_id)
        candidates = petreport.get_candidate_PetReports()
        #Get the candidate count for pagination purposes.
        candidates_count = len(candidates)                 
        paged_candidates = petreport.get_ranked_PetReports(candidates=candidates, page=page)  
        paged_candidates = [{   "ID": pr.id, 
                                "proposed_by_username": pr.proposed_by.user.username,
                                "pet_name": pr.pet_name, 
                                "pet_type": pr.pet_type, 
                                "img_path": pr.img_path.name } for pr in paged_candidates]

        #Serialize the PetReport into JSON for easy accessing.
        payload = json.dumps ({ "pet_reports_list":paged_candidates, 
                                "count":len(paged_candidates), 
                                "total_count": candidates_count})
        return HttpResponse(payload, mimetype="application/json")   
    else:
        raise Http404


@login_required
def match(request, petreport_id):
    if request.method == "GET":
        target_petreport = get_object_or_404(PetReport, pk=petreport_id)
        #Are there any candidates?
        candidates = target_petreport.get_candidate_PetReports()
        #Add the UserProfile to the PetReport's workers list.
        target_petreport.workers.add(request.user.userprofile)

        if not candidates:
            messages.info (request, "Sorry, there are no pet reports for the selected pet report to match. However, you have been added as a worker for this pet.")
            return redirect(URL_HOME)            

        #Get the candidate count for pagination purposes.
        candidates_count = len(candidates)

        #Serialize the PetReport into JSON for easy accessing.
        target_pr_json = target_petreport.to_JSON()
        pet_fields = target_petreport.pack_PetReport_fields()
        return render_to_response (HTML_MATCHING, { 'pet_fields': pet_fields,
                                                    "target_petreport":target_petreport, 
                                                    "candidates_count":candidates_count}, RequestContext(request))
    else:
        raise Http404

@login_required
def propose(request, target_petreport_id, candidate_petreport_id):
    print_info_msg ("PROPOSE MATCH: target:%s candidate:%s" % (target_petreport_id, candidate_petreport_id))

    #Grab the Target and Candidate PetReports first.
    target = get_object_or_404(PetReport, pk=target_petreport_id)
    candidate = get_object_or_404(PetReport, pk=candidate_petreport_id)

    if request.method == "POST" and request.POST["g-recaptcha-response"]:
        recaptcha = request.POST["g-recaptcha-response"]
        query_data = urllib.urlencode({"secret":settings.RECAPTCHA_SECRET, "response":recaptcha})
        response = urllib2.urlopen(settings.RECAPTCHA_SITEVERIFY, query_data)
        status = json.loads(response.read())

        if status["success"] != True:
            messages.error(request, "CAPTCHA was not correct. Please try again.")
            return redirect(URL_MATCHING)

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
                    return redirect(URL_MATCHING + target_petreport_id + "/")

                # add voting reputation points if the user didn't vote before for this duplicate petmatch
                # if (proposed_by not in result.up_votes.all()) and (proposed_by not in result.down_votes.all()):
                if pm.UserProfile_has_voted(userprofile) is False:
                    proposed_by.update_reputation("ACTIVITY_PETMATCH_UPVOTE")

                result.up_votes.add(proposed_by)
                result.save()
                messages.success(request, "Because there was an existing match between the two pet reports that you tried to match, You have successfully upvoted the existing pet match. Help spread the word about this match!")
                Activity.log_activity("ACTIVITY_PETMATCH_UPVOTE", proposed_by, source=result)

            elif outcome == PETMATCH_OUTCOME_NEW_PETMATCH:
                messages.success(request, "Congratulations - The pet match was successful - You have earned %d Pet Points! Thank you for your contribution in helping to match this pet. You can view your pet match in the home page and in your profile. Help spread the word about your match!" % ACTIVITIES["ACTIVITY_PETMATCH_PROPOSED"]["reward"])
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
                    return redirect(URL_MATCHING + target_petreport_id + "/")

                # add voting reputation points if the user didn't vote before for this duplicate petmatch
                if user_has_voted == False:
                    proposed_by.update_reputation("ACTIVITY_PETMATCH_UPVOTE")

                result.up_votes.add(proposed_by)
                result.save()          
                messages.success(request, "Because there was an existing match between the two pet reports that you tried to match, You have successfully upvoted the existing pet match. Help spread the word about this match!")
                Activity.log_activity("ACTIVITY_PETMATCH_UPVOTE", proposed_by, source=result)
            else:                
                messages.error(request, "A Problem was found when trying to propose the PetMatch. We have been notified of the issue and will fix it as soon as possible.")            

        #Finally, return the redirect.            
        return redirect(URL_HOME)
    
    else:
        if request.method == "POST" and not request.POST["g-recaptcha-response"]:
            messages.error(request, "Please Fill in the RECAPTCHA.")

        if request.is_ajax() == True:
            html = HTML_PROPOSE_MATCH
        else:
            html = HTML_PROPOSE_MATCH_FULL

        if (target.pet_type != candidate.pet_type) or (target.status == candidate.status) or (target.proposed_by == candidate.proposed_by):
            messages.error(request, "This proposal is invalid! Please try another one.")
            return redirect(URL_MATCHING + str(target.id))

        pet_fields = target.pack_PetReport_fields(other_pet=candidate)
        return render_to_response(html, { 'target':target, 
                                                             'candidate':candidate,
                                                             'pet_fields': pet_fields }, RequestContext(request))









