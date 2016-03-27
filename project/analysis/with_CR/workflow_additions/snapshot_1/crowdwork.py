from crowdrouter import AbstractCrowdRouter, AbstractWorkFlow, AbstractTask
from crowdrouter.decorators import *
from crowdrouter.task.abstract_crowd_choice import AbstractCrowdChoice
from reporting.models import PetReport
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from utilities.utils import recaptcha_ok, print_info_msg, print_error_msg, print_success_msg, send_email, generate_pet_contacts
from django.contrib import messages
from django.shortcuts import get_object_or_404
from reporting.constants import *
from home.constants import URL_HOME, HTML_HOME
from matching.constants import HTML_MATCHING, HTML_PMDP, URL_MATCHING, URL_PROPOSE_PETMATCH, URL_VOTE_PETMATCH, HTML_PROPOSE_MATCH, UPVOTE, DOWNVOTE, PETMATCH_OUTCOME_UPDATE, PETMATCH_OUTCOME_DUPLICATE_PETMATCH, PETMATCH_OUTCOME_NEW_PETMATCH
from home.models import Activity
from matching.models import PetMatch
from verifying.models import PetMatchCheck
from django.conf import settings
import ipdb

class MatchTask(AbstractTask):
    @task
    def get(self, crowd_request, data, **kwargs):
        if kwargs.get('pipe_data'):
            petreport_id = kwargs['pipe_data']['petreport_id']
            action = kwargs['pipe_data']["action"] #Specifies the endpoint that we're using.
        else:
            petreport_id = data["petreport_id"]
            action = URL_MATCHING + str(petreport_id)

        request = crowd_request.request_strategy.request
        target_petreport = get_object_or_404(PetReport, pk=petreport_id)
        #Are there any candidates?
        candidates_count = len(target_petreport.get_candidate_PetReports())
        #Add the UserProfile to the PetReport's workers list.
        target_petreport.workers.add(request.user.userprofile)

        if candidates_count == 0:
            messages.info (request, "Sorry, there are no pet reports for the selected pet report to match. However, you have been added as a worker for this pet.")
            return {"status":"fail", "path": HTML_HOME}
        return {
            "status": "ok",
            "action": action,
            "path": HTML_MATCHING,
            'target_petreport': target_petreport,
            'petreport_fields': target_petreport.get_display_fields(),
            "candidates_count":candidates_count
        }

    @task
    def post(self, crowd_request, data, form, **kwargs):
        if kwargs.get('pipe_data'):
            target_id = kwargs['pipe_data']['petreport_id']
            kwargs['pipe_data']['candidate_id'] = form['candidate_id'] #Cache the candidate ID.
        else:
            target_id = data["petreport_id"]

        candidate_id = form["candidate_id"]
        target = get_object_or_404(PetReport, pk=target_id)
        candidate = get_object_or_404(PetReport, pk=candidate_id)

        if (target.pet_type != candidate.pet_type) or (target.status == candidate.status):
            messages.error(request, "This proposal is invalid! Please try another one.")
            return {"status":"fail", "path": URL_MATCHING + str(target_id)}

        crowd_request.request_strategy.data.update({"target_id":target_id, "candidate_id":candidate_id})

        return {
            "status":"ok",
            "path": URL_PROPOSE_PETMATCH + str(target_id) + "/" + str(candidate_id),
            "target_id": target_id,
            "candidate_id": candidate_id
        }

class ProposeMatchTask(AbstractTask):
    @task
    def get(self, crowd_request, data, **kwargs):
        if not kwargs.get('pipe_data') and crowd_request.get_session()['cr_data']:
            kwargs['pipe_data'] = crowd_request.get_session()['cr_data']
        if kwargs.get('pipe_data'):
            target_id = kwargs['pipe_data']['petreport_id']
            candidate_id = kwargs['pipe_data']['candidate_id']
            action = kwargs['pipe_data']["action"] #Specifies the endpoint that we're using.
        else:
            target_id = crowd_request.get_data()["target_id"]
            candidate_id = crowd_request.get_data()["candidate_id"]
            action = URL_PROPOSE_PETMATCH + "%s/%s/" % (str(target_id), str(candidate_id))

        target = get_object_or_404(PetReport, pk=target_id)
        candidate = get_object_or_404(PetReport, pk=candidate_id)

        petreport_fields = [{
            'attr':a['attr'],
            'label':a['label'],
            'lost_pet_value':a['value'],
            'found_pet_value':b['value']
        } for a,b in zip(target.get_display_fields(), candidate.get_display_fields())]

        return {
            "status": "ok",
            "action": action,
            "path": HTML_PROPOSE_MATCH,
            "target": target,
            "candidate": candidate,
            "RECAPTCHA_CLIENT_SECRET": settings.RECAPTCHA_CLIENT_SECRET,
            "petreport_fields": petreport_fields
        }

    @task
    def post(self, crowd_request, data, form, **kwargs):
        if not kwargs.get('pipe_data') and crowd_request.get_session()['cr_data']:
            kwargs['pipe_data'] = crowd_request.get_session()['cr_data']
        if kwargs.get('pipe_data'):
            target_id = kwargs['pipe_data']['petreport_id']
            candidate_id = kwargs['pipe_data']['candidate_id']
        else:
            target_id = data["target_id"]
            candidate_id = data["candidate_id"]

        if form.get('no-match'): #If no match.
            return {"path": URL_HOME}

        target = get_object_or_404(PetReport, pk=target_id)
        candidate = get_object_or_404(PetReport, pk=candidate_id)
        request = crowd_request.request_strategy.request
        proposed_by = request.user.userprofile

        if not request.POST.get("g-recaptcha-response"):
            messages.error(request, "Please Fill in the RECAPTCHA.")
            return {"status":"fail", "path": URL_MATCHING + str(target_id)}

        if not recaptcha_ok(request.POST["g-recaptcha-response"]):
            messages.error(request, "CAPTCHA was not correct. Please try again.")
            return {"status":"fail", "path": URL_MATCHING + str(target_id)}

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
        return {"status": "ok", "path": URL_HOME, "pm": result}

class VoteTask(AbstractTask):
    @task
    def get(self, crowd_request, data, **kwargs):
        if kwargs.get('pipe_data'):
            petmatch_id = kwargs['pipe_data']['petmatch_id']
            action = kwargs['pipe_data']["action"] #Specifies the endpoint that we're using.
        else:
            petmatch_id = data["petmatch_id"]
            action = URL_VOTE_PETMATCH + str(petmatch_id)

        request = crowd_request.request_strategy.request
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
            "status":"ok",
            "action":action,
            "path": HTML_PMDP,
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
        return ctx

    @task
    def post(self, crowd_request, data, form, **kwargs):
        if kwargs.get('pipe_data'):
            petmatch_id = kwargs['pipe_data']['petmatch_id']
            action = kwargs['pipe_data']["action"] #Specifies the endpoint that we're using.
        else:
            petmatch_id = data["petmatch_id"]
            action = URL_VOTE_PETMATCH

        if form.get('up') != None:
            vote = "upvote"
        else:
            vote = "downvote"

        request = crowd_request.request_strategy.request
        userprofile = request.user.userprofile
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

        return {
            "status":"ok",
            "vote":vote,
            "path": URL_HOME,
            "message": message,
            "threshold_reached": threshold_reached,
            "num_downvotes": num_downvotes,
            "num_upvotes": num_upvotes
        }

class MatchingWorkFlow(AbstractWorkFlow):
    tasks = [MatchTask, ProposeMatchTask]
    def __init__(self, cr):
        self.crowdrouter = cr
    @workflow
    def run(self, task, crowd_request):
        return self.pipeline(crowd_request)

class VotingWorkFlow(AbstractWorkFlow):
    tasks = [VoteTask]
    def __init__(self, cr):
        self.crowdrouter = cr
    @workflow
    def run(self, task, crowd_request):
        return task.execute(crowd_request)

class EPMCrowdRouter(AbstractCrowdRouter):
    workflows = [MatchingWorkFlow, VotingWorkFlow, MixedWorkFlow, ChoiceWorkFlow]
    def __init__(self):
        self.enable_crowd_statistics("crowd_stats.db")
    @crowdrouter
    def route(self, workflow, crowd_request):
        return workflow.run(crowd_request)
