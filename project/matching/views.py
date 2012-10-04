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
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.models import model_to_dict
from social_auth import __version__ as version
from social_auth.utils import setting
from social_auth.views import auth
from random import choice, uniform
from django.utils import simplejson
from home.models import *
from constants import *
from logging import *
import datetime, re


''' Display the PetMatch object '''
def display_PetMatch(request, petmatch_id):

    pm = get_object_or_404(PetMatch, pk=petmatch_id)
    voters = list(pm.up_votes.all()) + list(pm.down_votes.all())

    #Need to check if the user is authenticated (non-anonymous) to find out if he/she has voted on this PetMatch.
    if request.user.is_authenticated() == True:
        user_has_voted = pm.UserProfile_has_voted(request.user.get_profile())
    else:
        user_has_voted = False

    num_upvotes = len(pm.up_votes.all())
    num_downvotes = len(pm.down_votes.all())

    return render_to_response(HTML_PMDP, {'petmatch': pm, "voters": voters, "user_has_voted": user_has_voted, "num_upvotes":num_upvotes, "num_downvotes":num_downvotes},
         RequestContext(request))  

@login_required
def vote_PetMatch(request):
    
    if request.method == "POST":
        userprofile = request.user.get_profile()
        vote = request.POST ['vote']
        pm = get_object_or_404(PetMatch, pk=request.POST["match_id"])

        print "VOTE: %s" % vote
        print "#UPVOTES: %d" % len(pm.up_votes.all())
        print "#DOWNVOTES: %d" % len(pm.down_votes.all())

        if vote == "upvote":
            pm.up_votes.add(userprofile)
            pm.down_votes.remove(userprofile)
            log_activity(ACTIVITY_PETMATCH_UPVOTE, userprofile, petmatch=pm)
            message = "You have successfully upvoted this PetMatch!"

            '''Checking condition that will return true once PetMatch reaches a threshold value,
            if it returns true, pet match verification work flow is triggered'''
            '''convert this to a signal '''
            if pm.PetMatch_has_reached_threshold():
                pm.verify_petmatch()   
        elif vote == "downvote":
            pm.down_votes.add(userprofile)
            pm.up_votes.remove(userprofile)
            log_activity(ACTIVITY_PETMATCH_DOWNVOTE, userprofile, petmatch=pm)
            message = "You have successfully downvoted this PetMatch!"
        else:
            message = "There was something wrong with this vote. Please let us know by emailing us at emergencypetmatcher@gmail.com"

        num_upvotes = len(pm.up_votes.all())
        num_downvotes = len(pm.down_votes.all())

        
        json = simplejson.dumps ({"vote":vote, "message":message, "num_downvotes":num_downvotes, "num_upvotes":num_upvotes})
        print "JSON: " + str(json)
        return HttpResponse(json, mimetype="application/json")

    else:
        raise Http404

@login_required
def match_PetReport(request, petreport_id):

	#Get Pet Report objects and organize them into a Paginator Object.
    target_petreport = get_object_or_404(PetReport, pk=petreport_id)

    all_pet_reports = PetReport.objects.all().exclude(pk=petreport_id)
    if len(all_pet_reports) == 0:
        messages.info (request, "Sorry, there are no pet reports to match!")
        return redirect(URL_HOME)

    #Place more PetReport filters here
    filtered_pet_reports = all_pet_reports.exclude(status = target_petreport.status).filter(pet_type = target_petreport.pet_type)

    if len(filtered_pet_reports) == 0:
        messages.info (request, "Sorry, there are no pet reports for the selected pet report to match!")
        return redirect(URL_HOME)

    paginator = Paginator(filtered_pet_reports, 100)
    page = request.GET.get('page')
  
    try:
        pet_reports_list = paginator.page(page)
    except PageNotAnInteger:
        pet_reports_list = paginator.page(1)
    except EmptyPage:
        pet_reports_list = paginator.page(paginator.num_pages)

    return render_to_response (HTML_MATCHING, {'target_petreport':target_petreport, 'pet_reports_list': pet_reports_list}, RequestContext(request))


@login_required
def propose_PetMatch(request, target_petreport_id, candidate_petreport_id):

    print "PROPOSE MATCH: target:%s candidate:%s" % (target_petreport_id, candidate_petreport_id)

    #Grab the Target and Candidate PetReports first.
    target = get_object_or_404(PetReport, pk=target_petreport_id)
    candidate = get_object_or_404(PetReport, pk=candidate_petreport_id)

    if request.method == "POST":
        description = request.POST ["description"].strip()

        if description == "":
            messages.error (request, "Please fill out a description for this PetMatch proposal.")
            return render_to_response(HTML_PROPOSE_MATCH, {'target':target, 'candidate':candidate}, RequestContext(request))

        proposed_by = request.user.get_profile()

        if target.status == "Lost":
            pm = PetMatch(lost_pet=target, found_pet=candidate, proposed_by=proposed_by, description=description)
        else:
            pm = PetMatch(lost_pet=candidate, found_pet=target, proposed_by=proposed_by, description=description)

        #Try saving the PetMatch object.
        # We will expect the following output:
        # None --> PetMatch was not inserted properly OR Duplicate PetMatch
        # PetMatch Object --> Existing PetMatch (UPDATE) OR Brand new PetMatch.
        # "Existing" means the PetMatch to be saved is the same PetMatch found, "Duplicate" means
        # another PetMatch with the same Lost+Found Pets were found.
        (result, outcome) = pm.save()

        if result != None:
            if outcome == "SQL UPDATE": 
                #Has the user voted for this PetMatch before?
                user_has_voted = result.UserProfile_has_voted(proposed_by)

                if user_has_voted == "UPVOTE" or user_has_voted == "DOWNVOTE":
                    messages.error(request, "This Pet Match has already been proposed, and you have already voted for it already!")
                    return redirect(URL_MATCHING + target_petreport_id + "/")

                result.up_votes.add(proposed_by)
                result.save()
                messages.success(request, "Nice job! Because there was an existing match between the two pet reports that you tried to match, You have successfully upvoted the existing pet match.\nHelp spread the word about your match by sharing it on Facebook and on Twitter!")
                log_activity(ACTIVITY_PETMATCH_UPVOTE, proposed_by, petmatch=result)

            elif outcome == "NEW PETMATCH":
                #Verification votes is initialized to 00 if the user who proposed the pet match is the same user who proposed the target or candidate pet report
                if (target.proposed_by == proposed_by) or (candidate.proposed_by == proposed_by):
                    pm.verification_votes='00'
                else: 
                    pm.verification_votes='000'
                (result,outcome) = pm.save()
                messages.success(request, "Congratulations - The pet match was successful! Thank you for your contribution in helping to match this pet. You can view your pet match in the home page and in your profile.\nHelp spread the word about your match by sharing it on Facebook and on Twitter!")
                log_activity(ACTIVITY_PETMATCH_PROPOSED, proposed_by, petmatch=pm)

        else:
            if outcome == "DUPLICATE PETMATCH":
                result = PetMatch.get_PetMatch(target, candidate)
                #Has the user voted for this PetMatch before?
                user_has_voted = result.UserProfile_has_voted(proposed_by)

                if user_has_voted == "UPVOTE" or user_has_voted == "DOWNVOTE":
                    messages.error(request, "This Pet Match has already been proposed, and you have already voted for it already!")
                    return redirect(URL_MATCHING + target_petreport_id + "/")

                result.up_votes.add(proposed_by)
                result.save()                
                messages.success(request, "Nice job! Because there was an existing match between the two pet reports that you tried to match, You have successfully upvoted the existing pet match.\nHelp spread the word about your match by sharing it on Facebook and on Twitter!")
                log_activity(ACTIVITY_PETMATCH_UPVOTE, proposed_by, petmatch=result)
            else:                
                messages.error(request, "A Problem was found when trying to propose the PetMatch. We have been notified of the issue and will fix it as soon as possible.")            

        #Finally, return the redirect.            
        return redirect(URL_HOME)
    
    else:
        return render_to_response(HTML_PROPOSE_MATCH, {'target':target, 'candidate':candidate}, RequestContext(request))

@login_required
def verify_PetMatch(request, petmatch_id):
    if request.method == "GET":
        pm = get_object_or_404(PetMatch, pk=petmatch_id)
        voters = list(pm.up_votes.all()) + list(pm.down_votes.all())

        #Need to check if the user is authenticated (non-anonymous) to find out if he/she has voted on this PetMatch.
        if request.user.is_authenticated() == True:
            user_has_voted = pm.UserProfile_has_voted(request.user.get_profile())
        else:
            user_has_voted = False

        num_upvotes = len(pm.up_votes.all())
        num_downvotes = len(pm.down_votes.all())
        return render_to_response(HTML_VERIFY_PETMATCH,{'petmatch': pm, "voters": voters, "user_has_voted": user_has_voted, "num_upvotes":num_upvotes, "num_downvotes":num_downvotes}, RequestContext(request))
    elif request.method == "POST":
        pm = get_object_or_404(PetMatch, pk=petmatch_id)
        action = request.POST['message']
        if action[0] == 'y':
            bit = '1'
        else:
            bit = '2'     
        pm.verification_votes = '00'
        if pm.verification_votes[0] == '0':
            pm.verification_votes = bit+pm.verification_votes[1]
        elif pm.verification_votes[1] == '0':
            pm.verification_votes = pm.verification_votes[0]+bit
        print 'votes bits: '+str(pm.verification_votes)
        pm.save() 
        if '0' not in pm.verification_votes:
            pm.close_PetMatch()
            message = "Thank you, your input has been recorded. This pet match is now closed."
        else:
            message = "Thank you, your input has been recorded. Once your peers verify this petmatch, it will be closed."
        return render_to_response(HTML_HOME, {'message':message}, RequestContext(request))
