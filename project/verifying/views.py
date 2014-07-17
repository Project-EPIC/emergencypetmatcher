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
from django.utils import simplejson
from social_auth import __version__ as version
from social_auth.utils import setting
from social_auth.views import auth
from random import choice, uniform
from pprint import pprint
from reporting.models import PetReport
from matching.models import PetMatch
from utilities.utils import *
from utilities import logger
from matching.constants import *
from home.constants import *
import datetime, re

@login_required
def verify_PetMatch(request, petmatch_id):
    pm = get_object_or_404(PetMatch, pk=petmatch_id)
    profile = request.user.get_profile()    

    #This page cannot be rendered if the threshold has not been reached and is only accessible by either the found pet contact or the lost pet contact.
    if  (pm.verification_triggered == True) and ((profile == pm.lost_pet.proposed_by) or (profile == pm.found_pet.proposed_by)):

        #GET Verification Page.
        if request.method == "GET":
            voters = list(pm.up_votes.all()) + list(pm.down_votes.all())
            num_upvotes = len(pm.up_votes.all())
            num_downvotes = len(pm.down_votes.all())
            user_has_voted = pm.UserProfile_has_voted(profile)
            user_is_owner = (profile == pm.lost_pet.proposed_by) or False
            pos = 0 if (profile == pm.lost_pet.proposed_by) else 1
            if pm.verification_votes[pos] != '0':
                user_has_verified = True
            else:
                user_has_verified = False

            return render_to_response(HTML_VERIFY_PETMATCH,{'petmatch': pm,
                                                            "voters": voters, 
                                                            "num_upvotes":num_upvotes, 
                                                            "user_is_owner":user_is_owner,
                                                            "user_has_voted":user_has_voted, 
                                                            "num_downvotes":num_downvotes, 
                                                            "user_has_verified":user_has_verified}, RequestContext(request))
        #POST for Verification.    
        elif request.method == "POST":
            action = request.POST['choice']
            bit = 1 if (action == 'Yes') else 2 if (action == 'No') else 0
            pos = 0 if (profile == pm.lost_pet.proposed_by) else 1

            #User cannot change his/her response once it has been submitted
            if pm.verification_votes[pos] != '0':
                messages.error(request, "You have already submitted a response for this PetMatch!")
                return redirect(URL_HOME)
            if pos == 0:
                pm.verification_votes = str(bit) + pm.verification_votes[1]
            else:
                pm.verification_votes = pm.verification_votes[0] + str(bit)

            pm.save()

            #Have we completed verification? 
            if '0' not in pm.verification_votes:
                message = pm.close_PetMatch()
                messages.success(request, message)
            else:
                messages.success(request, "Thanks for your response! Once the other pet contact verifies this petmatch, it will be closed.")
            return redirect(URL_HOME)

        else: 
            messages.error(request,"This pet match is not yet eligible for verification, please wait for an email from us. Thank you.")
            return redirect(URL_HOME)
    else:
        messages.error(request, "Sorry, you don't have access to this page.")
        return redirect(URL_HOME)

