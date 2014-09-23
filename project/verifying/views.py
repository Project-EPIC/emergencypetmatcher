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
from reporting.models import PetReport
from verifying.models import PetCheck
from matching.models import PetMatch
from utilities.utils import *
from verifying.constants import *
from home.constants import *
import datetime, re, json

def verify_PetCheck(request, petcheck_id):
    petcheck = get_object_or_404(PetCheck, pk=petcheck_id)
    petmatch = petcheck.petmatch
    lost_pet = petmatch.lost_pet
    found_pet = petmatch.found_pet
    pet_fields = lost_pet.pack_PetReport_fields(other_pet=found_pet)

    if request.user.is_anonymous() == True:
        profile = None
    else:
        profile = request.user.userprofile

    if request.method == "GET":
        num_upvotes = len(petmatch.up_votes.all())
        num_downvotes = len(petmatch.down_votes.all())        
        user_has_verified = False
        user_has_voted = False
        user_is_owner = False
        
        if profile != None:
            user_has_voted = petmatch.UserProfile_has_voted(profile)
            user_has_verified = petcheck.UserProfile_has_verified(profile)

            #Need to determine if lost pet proposer truly is owner or just crossposter.
            if profile == lost_pet.proposed_by:
                if lost_pet.is_crossposted() == True:
                    user_is_owner = False #just crossposter.
                else: 
                    user_is_owner = True #owner.

        return render_to_response(HTML_VERIFY_PETCHECK, {   "petcheck": petcheck,
                                                            "petmatch": petmatch,
                                                            "pet_fields": pet_fields,
                                                            "lost_petreport_id": lost_pet.id,
                                                            "found_petreport_id": found_pet.id,
                                                            "profile": profile,
                                                            "contacts": [lost_pet.proposed_by, found_pet.proposed_by],
                                                            "num_voters": num_upvotes + num_downvotes,
                                                            "user_is_owner": user_is_owner,
                                                            "user_has_voted": user_has_voted,
                                                            "user_has_verified": user_has_verified}, RequestContext(request))
    #POST for Verification.
    elif request.method == "POST":
        pprint(request.POST)
        choice = request.POST['verify-choice']

        if profile == lost_pet.proposed_by:
            petcheck.verification_votes = choice + petcheck.verification_votes[1]
        else:
            petcheck.verification_votes = petcheck.verification_votes[0] + choice

        petcheck.save()

        #Have we completed verification? 
        if petcheck.verification_complete() == True:
            message = petcheck.close_PetMatch()
            messages.success(request, message)
        else:
            messages.success(request, "Thanks for your response! Once the other pet contact verifies this petmatch, it will be closed.")
        return redirect(URL_HOME)

    else: 
        messages.error(request,"This pet match is not yet eligible for verification, please wait for an email from us. Thank you.")
        return redirect(URL_HOME)






