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
from django.http import JsonResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from pprint import pprint
from reporting.models import PetReport
from verifying.models import PetMatchCheck, PetReunion, PetReunionForm
from matching.models import PetMatch
from utilities.utils import *
from verifying.constants import *
from verifying.decorators import *
from home.constants import *
import datetime, re, json, pdb

def get_PetReunion(request, petreunion_id):
    pet_reunion = get_object_or_404(PetReunion, pk=petreunion_id)
    num_workers = len(pet_reunion.petreport.workers.all())
    pet_has_been_successfully_matched = pet_reunion.petreport.has_been_successfully_matched()
    return render_to_response(HTML_PETREUNION, {
        "pet_reunion":pet_reunion,
        "pet_report":pet_reunion.petreport,
        'petreunion_fields': pet_reunion.get_display_fields(),
        "reason": pet_reunion.get_display_reason(),
        "long_reason":pet_reunion.get_long_reason(),
        "matched": pet_has_been_successfully_matched,
    }, RequestContext(request))

#Given a PetReport ID, just return the PetReport JSON.
def get_PetReunion_JSON(request):
    if (request.method == "GET") and (request.is_ajax() == True):
        petreunion = get_object_or_404(PetReunion, pk=request.GET.get("petreunion_id"))
        return JsonResponse({"petreunion":petreunion.to_DICT()}, safe=False)
    else:
        raise Http404

#Given a Page Number, return a list of PetReports.
def get_PetReunions_JSON(request):
    if request.is_ajax() == True:
        page = int(request.GET["page"])
        filters = dict(request.GET)
        filters.pop("page")
        filters = {k:v[0].strip() for k,v in filters.items()}
        pet_reunions = PetReunion.objects.filter(**filters).order_by("id").reverse()
        petreunion_count = len(pet_reunions)
        pet_reunions = get_objects_by_page(pet_reunions, page, limit=NUM_PETREUNIONS_HOMEPAGE)
        pet_reunions = [{
            "ID"                    : pr.id,
            "proposed_by_username"  : pr.petreport.proposed_by.user.username,
            "pet_name"              : pr.petreport.pet_name,
            "img_path"              : pr.thumb_path.name,
            "reason"                : pr.get_display_reason()
        } for pr in pet_reunions]

        return JsonResponse({"pet_reunions_list":pet_reunions, "count":len(pet_reunions), "total_count": petreunion_count}, safe=False)
    else:
        raise Http404

@login_required
@allow_only_checkers
def verify(request, petmatchcheck_id):
    petmatchcheck = get_object_or_404(PetMatchCheck, pk=petmatchcheck_id)
    petmatch = petmatchcheck.petmatch
    lost_pet = petmatch.lost_pet
    found_pet = petmatch.found_pet
    profile = request.user.userprofile

    if request.method == "GET":
        user_is_owner = False
        user_has_voted = petmatch.UserProfile_has_voted(profile)
        user_has_verified = petmatchcheck.UserProfile_has_verified(profile)
        #Need to determine if lost pet proposer truly is owner or just crossposter.
        if profile == lost_pet.proposed_by:
            if lost_pet.is_crossposted() == True:
                user_is_owner = False #just crossposter.
            else:
                user_is_owner = True #owner.

        return render_to_response(HTML_VERIFY_PETMATCHCHECK, {
            "petmatchcheck": petmatchcheck,
            "petmatch": petmatch,
            "petreport_fields": petmatch.get_display_fields(),
            "lost_petreport_id": lost_pet.id,
            "found_petreport_id": found_pet.id,
            "profile": profile,
            "contacts": [lost_pet.proposed_by, found_pet.proposed_by],
            "num_voters": petmatch.up_votes.count() + petmatch.down_votes.count(),
            "user_is_owner": user_is_owner,
            "user_has_voted": user_has_voted,
            "user_has_verified": user_has_verified
        }, RequestContext(request))

    elif request.method == "POST":
        choice = request.POST['verify-choice']

        if profile == lost_pet.proposed_by:
            petmatchcheck.verification_votes = choice + petmatchcheck.verification_votes[1]
        else:
            petmatchcheck.verification_votes = petmatchcheck.verification_votes[0] + choice

        petmatchcheck.save()
        if petmatchcheck.verification_complete() == True:
            if petmatchcheck.close_PetMatch() == True:
                if profile == lost_pet.proposed_by:
                    #Send mail to Lost Pet Contact after verification.
                    email_body = render_to_string(TEXTFILE_EMAIL_CLOSE_PETREPORT_BODY, {"site": Site.objects.get_current(), "reunited_pet":lost_pet })
                    send_mail(TEXTFILE_EMAIL_CLOSE_PETREPORT_SUBJECT, email_body, None, [profile.user.email])
                    messages.success(request, "Congratulations on the successful match! Please look out for an email to close your pet report.")
                else:
                    messages.success(request, "Thanks for your response, and congratulations on the successful match!")
            else:
                messages.success(request, "Unfortunately, this Pet Match was not successful. The pet contacts have agreed that this wasn't the right match. Please try other matches!")
        else:
            messages.success(request, "Thanks for your response! Once the other pet contact verifies this petmatch, it will be closed.")
        return redirect(URL_HOME)
    else:
        raise Http404
