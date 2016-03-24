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
from crowdwork import EPMCrowdRouter
import datetime, re, json, ipdb, urllib, urllib2, ssl

#Display the PetMatch object
def get(request, petmatch_id):
    cr = EPMCrowdRouter()
    response = cr.route("VotingWorkFlow", "VoteTask", request, petmatch_id=petmatch_id).response
    return render_to_response(response["path"], response, RequestContext(request))

@login_required
@allow_only_before_closing
def vote(request, petmatch_id):
    cr = EPMCrowdRouter()
    response = cr.route("VotingWorkFlow", "VoteTask", request, petmatch_id=petmatch_id).response
    messages.success(request, response["message"])
    return redirect(URL_HOME)

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
def new(request, petreport_id):
    cr = EPMCrowdRouter()
    response = cr.route("MatchingWorkFlow", "MatchTask", request, petreport_id=petreport_id).response
    return render_to_response(response["path"], response, RequestContext(request))

@login_required
@disallow_closed_petreports
@disallow_incompatible_petreports
def propose(request, target_id, candidate_id):
    cr = EPMCrowdRouter()
    response = cr.route("MatchingWorkFlow", "ProposeMatchTask", request, target_id=target_id, candidate_id=candidate_id).response
    if request.method == "GET":
        return render_to_response(response["path"], response, RequestContext(request))
    else:
        return redirect(response["path"])
