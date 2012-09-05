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
import datetime, re
import utils

''' Display the PetMatch object '''
def display_PetMatch(request, petmatch_id):

    pm = get_object_or_404(PetMatch, pk=petmatch_id)
    voters = list(pm.up_votes.all()) + list(pm.down_votes.all())

    #Need to check if the user is authenticated (non-anonymous) to find out if he/she has voted on this PetMatch.
    if request.user.is_authenticated() == True:
        user_has_voted = pm.UserProfile_has_voted(request.user.get_profile())
    else:
        user_has_voted = False

    return render_to_response('matching/petmatch.html', {'petmatch': pm, "voters": voters, "user_has_voted": user_has_voted}, RequestContext(request))  

@login_required
def vote_PetMatch(request):
    
    if request.method == "POST":
        userprofile = request.user.get_profile()
        vote = request.POST ['vote']

        #TODO: Retrieve the PetMatch, up/down-vote it. 
        pm = get_object_or_404(PetMatch, pk=request.POST["match_id"])

        if vote == "upvote":
            pm.up_votes.add(userprofile)
            pm.down_votes.remove(userprofile)
            log_activity(ACTIVITY_PETMATCH_UPVOTE, userprofile, petmatch=pm)
        else:
            pm.down_votes.add(userprofile)
            pm.up_votes.remove(userprofile)
            log_activity(ACTIVITY_PETMATCH_DOWNVOTE, userprofile, petmatch=pm)

        message = "You have successfully %sd this PetMatch!" % vote            
        json = simplejson.dumps ({"vote":vote, "message":message})
        print "JSON: " + str(json)
        return HttpResponse(json, mimetype="application/json")

    else:
        raise Http404

@login_required
def match_PetReport(request, petreport_id):

	#Get Pet Report objects and organize them into a Paginator Object.
    target_petreport = get_object_or_404(PetReport, pk=petreport_id)

    #Place more PetReport filters here
    all_pet_reports = PetReport.objects.all().exclude(pk=petreport_id)
    if len(all_pet_reports) == 0:
        messages.info (request, "Sorry, there are no pet reports to match!")
        return redirect("/")

    filtered_pet_reports = all_pet_reports.exclude(status = target_petreport.status).filter(pet_type = target_petreport.pet_type)

    if len(filtered_pet_reports) == 0:
        messages.info (request, "Sorry, there are no pet reports for the selected pet report to match!")
        return redirect("/")

    paginator = Paginator(filtered_pet_reports, 100)
    page = request.GET.get('page')
  
    try:
        pet_reports_list = paginator.page(page)
    except PageNotAnInteger:
        pet_reports_list = paginator.page(1)
    except EmptyPage:
        pet_reports_list = paginator.page(paginator.num_pages)

    return render_to_response ('matching/matching.html', {'target_petreport':target_petreport, 'pet_reports_list': pet_reports_list}, RequestContext(request))


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
            return render_to_response('matching/propose_match.html', {'target':target, 'candidate':candidate}, RequestContext(request))

        proposed_by = request.user.get_profile()
        pm = None #Our PetMatch object.
        #Let's try to find an already existing PetMatch for the target and candidate
        existing_match = PetMatch.get_PetMatch (target, candidate)

        #No existing match to worry about; create the PetMatch.
        if existing_match == None:
            if target.status == "Lost":
                pm = PetMatch(lost_pet=target, found_pet=candidate, description=description, proposed_by=proposed_by)
            else:
                pm = PetMatch(lost_pet=candidate, found_pet=target, description=description, proposed_by=proposed_by)

            pm.save()
            messages.success(request, "Congratulations - The pet match was successful! Thank you for your contribution in helping to match this pet. You can view your pet match in the home page and in your profile.\nHelp spread the word about your match by sharing it on Facebook and on Twitter!")
            log_activity(ACTIVITY_PETMATCH_PROPOSED, proposed_by, petmatch=pm)

        #A PetMatch already exists.            
        else:
            #Has the user voted for this PetMatch before?
            user_has_voted = existing_match.UserProfile_has_voted(proposed_by)

            if user_has_voted == "upvote" or user_has_voted == "down-vote":
                messages.error(request, "You have already voted for this PetMatch already!")
                return redirect("/matching/match_PetReport/%s/" % (target_petreport_id))

            existing_match.up_votes.add(proposed_by)
            existing_match.save()
            messages.success(request, "Nice job! Because there was an existing match between the two pet reports with which you proposed a match, You have successfully upvoted the existing petmatch.\nHelp spread the word about your match by sharing it on Facebook and on Twitter!")
            log_activity(ACTIVITY_PETMATCH_UPVOTE, proposed_by, petmatch=existing_match)

        return redirect("/")

    else:
        return render_to_response('matching/propose_match.html', {'target':target, 'candidate':candidate}, RequestContext(request))











