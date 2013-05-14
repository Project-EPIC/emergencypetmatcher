'''django imports'''
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
from django.utils import simplejson
#django project imports
#django plugin imports
from social_auth import __version__ as version
from social_auth.utils import setting
from social_auth.views import auth
#python imports
from random import choice, uniform
from utils import *
import datetime, re, home.logger

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

        print_info_msg ("VOTE: %s" % vote)
        print_info_msg ("#UPVOTES: %d" % len(pm.up_votes.all()))
        print_info_msg ("#DOWNVOTES: %d" % len(pm.down_votes.all()))

        if vote == "upvote":
            # If the user is voting for the 1st time, add reputation points
            if pm.UserProfile_has_voted(userprofile) is False:
                userprofile.update_reputation(ACTIVITY_PETMATCH_UPVOTE)
                pm.proposed_by.update_reputation(ACTIVITY_USER_PROPOSED_PETMATCH_UPVOTE)

            # Also, add reputation points to the user whose proposed petmatch is being upvoted
            if pm.UserProfile_has_voted(userprofile) == DOWNVOTE:
                pm.proposed_by.update_reputation(ACTIVITY_USER_PROPOSED_PETMATCH_UPVOTE)
            
            pm.up_votes.add(userprofile)
            pm.down_votes.remove(userprofile)
            logger.log_activity(ACTIVITY_PETMATCH_UPVOTE, userprofile, petmatch=pm)
            message = "You have successfully upvoted this PetMatch!"
        elif vote == "downvote":
            # If the user is voting for the 1st time, add reputation points
            if pm.UserProfile_has_voted(userprofile) is False:
                userprofile.update_reputation(ACTIVITY_PETMATCH_DOWNVOTE)
                
            pm.down_votes.add(userprofile)
            pm.up_votes.remove(userprofile)
            logger.log_activity(ACTIVITY_PETMATCH_DOWNVOTE, userprofile, petmatch=pm)
            message = "You have successfully downvoted this PetMatch!"
        else:
            message = "There was something wrong with this vote. Please let us know by emailing us at emergencypetmatcher@gmail.com"

        num_upvotes = len(pm.up_votes.all())
        num_downvotes = len(pm.down_votes.all())

        
        json = simplejson.dumps ({"vote":vote, "message":message, "num_downvotes":num_downvotes, "num_upvotes":num_upvotes})
        print_info_msg ("JSON: " + str(json))
        return HttpResponse(json, mimetype="application/json")

    else:
        raise Http404

@login_required
def match_PetReport(request, petreport_id):

    #Get Pet Report objects and organize them into a Paginator Object.
    target_petreport = get_object_or_404(PetReport, pk=petreport_id)

    #Add the UserProfile to the PetReport's workers list.
    target_petreport.workers.add(request.user.get_profile())

    all_pet_reports = PetReport.objects.all().exclude(pk=petreport_id)

    #Place more PetReport filters here
    filtered_pet_reports = all_pet_reports.exclude(status = target_petreport.status).filter(pet_type = target_petreport.pet_type, closed = False)   

    if len(filtered_pet_reports) == 0:
        messages.info (request, "Sorry, there are no pet reports for the selected pet report to match. However, you have been added to this pet's working list for future reference.")
        return redirect(URL_HOME)
    
    pet_reports_list = []    
    matches = {"match6":[], "match5":[],"match4":[],"match3":[],"match2":[],"match1":[],"match0":[]}
    for candidate in filtered_pet_reports:
        num_attributes_matched = target_petreport.compare(candidate)
        #We use the num_attributes_matched to make our dictionary key.
        matches["match" + str(num_attributes_matched)].append(candidate)

    for key in matches.keys():
        pet_reports_list += matches[key]
    
    return render_to_response (HTML_MATCHING, {'target_petreport':target_petreport, 'candidate_matches': pet_reports_list}, RequestContext(request))


@login_required
def propose_PetMatch(request, target_petreport_id, candidate_petreport_id):
    print_info_msg ("PROPOSE MATCH: target:%s candidate:%s" % (target_petreport_id, candidate_petreport_id))

    #Grab the Target and Candidate PetReports first.
    target = get_object_or_404(PetReport, pk=target_petreport_id)
    candidate = get_object_or_404(PetReport, pk=candidate_petreport_id)

    if request.method == "POST":
        description = request.POST ["description"].strip()

        # if description == "":
        #     messages.error (request, "Please fill out a description for this PetMatch proposal.")
        #     return render_to_response(HTML_PROPOSE_MATCH, {'target':target, 'candidate':candidate}, RequestContext(request))

        proposed_by = request.user.get_profile()

        if target.status == "Lost":
            pm = PetMatch(lost_pet=target, found_pet=candidate, proposed_by=proposed_by, description=description)
        else:
            pm = PetMatch(lost_pet=candidate, found_pet=target, proposed_by=proposed_by, description=description)

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
                    proposed_by.update_reputation(ACTIVITY_PETMATCH_UPVOTE)

                result.up_votes.add(proposed_by)
                result.save()
                messages.success(request, "Nice job! Because there was an existing match between the two pet reports that you tried to match, You have successfully upvoted the existing pet match.\nHelp spread the word about your match by sharing it on Facebook and on Twitter!")
                logger.log_activity(ACTIVITY_PETMATCH_UPVOTE, proposed_by, petmatch=result)

            elif outcome == PETMATCH_OUTCOME_NEW_PETMATCH:
                messages.success(request, "Congratulations - The pet match was successful! Thank you for your contribution in helping to match this pet. You can view your pet match in the home page and in your profile.\nHelp spread the word about your match by sharing it on Facebook and on Twitter!")
                logger.log_activity(ACTIVITY_PETMATCH_PROPOSED, proposed_by, petmatch=result)
                # add reputation points for proposing a new petmatch
                proposed_by.update_reputation(ACTIVITY_PETMATCH_PROPOSED)

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
                    proposed_by.update_reputation(ACTIVITY_PETMATCH_UPVOTE)

                result.up_votes.add(proposed_by)
                result.save()          
                messages.success(request, "Nice job! Because there was an existing match between the two pet reports that you tried to match, You have successfully upvoted the existing pet match.\nHelp spread the word about your match by sharing it on Facebook and on Twitter!")
                logger.log_activity(ACTIVITY_PETMATCH_UPVOTE, proposed_by, petmatch=result)
            else:                
                messages.error(request, "A Problem was found when trying to propose the PetMatch. We have been notified of the issue and will fix it as soon as possible.")            

        #Finally, return the redirect.            
        return redirect(URL_HOME)
    
    else:
        return render_to_response(HTML_PROPOSE_MATCH, {'target':target, 'candidate':candidate}, RequestContext(request))

@login_required
def verify_PetMatch(request, petmatch_id):
    pm = get_object_or_404(PetMatch, pk=petmatch_id)
    user= request.user.get_profile()    
    '''This page is only accessible by either the found pet contact or the lost pet contact'''
    if  (user == pm.lost_pet.proposed_by) or (user == pm.found_pet.proposed_by):
        '''this page cannot be rendered if the threshold has not been reached'''
        if pm.verification_triggered == True:
            if request.method == "GET":
                voters = list(pm.up_votes.all()) + list(pm.down_votes.all())
                num_upvotes = len(pm.up_votes.all())
                num_downvotes = len(pm.down_votes.all())
                pos = 0 if (user == pm.lost_pet.proposed_by) else 1
                if pm.verification_votes[pos] != '0':
                    user_has_verified = "true"
                else:
                    user_has_verified = "false"
                ctx = {'petmatch': pm, "voters": voters, "num_upvotes":num_upvotes, "num_downvotes":num_downvotes,"user_has_verified":user_has_verified}
                return render_to_response(HTML_VERIFY_PETMATCH,ctx, RequestContext(request))

            elif request.method == "POST":
                pm = get_object_or_404(PetMatch, pk=petmatch_id)
                action = request.POST['message']    
                bit = 1 if (action == 'yes') else 2 if (action == 'no') else 0
                pos = 0 if (user == pm.lost_pet.proposed_by) else 1

                #User cannot change his/her response once it has been submitted
                if pm.verification_votes[pos] != '0':
                    messages.error(request, "You have already submitted a response for this PetMatch!")
                    return redirect(URL_HOME)
                if pos == 0:
                    pm.verification_votes = str(bit)+pm.verification_votes[1]
                else:
                    pm.verification_votes = pm.verification_votes[0]+str(bit)

                pm.save() 
                if '0' not in pm.verification_votes:
                    pm.close_PetMatch()
                    message = "Thank you, your input has been recorded. This pet match is now closed."
                else:
                    message = "Thank you, your input has been recorded. Once your peer verifies this petmatch, it will be closed."
                messages.success(request,message)
                return redirect(URL_HOME)
        else: 
            messages.error(request,"This pet match is not yet eligible for verification, please wait for an email from us. Thank you.")
            return redirect(URL_HOME)
    

    else:
        messages.error(request,"You do not have access to the verification page for that pet match!")
        return redirect(URL_HOME)
