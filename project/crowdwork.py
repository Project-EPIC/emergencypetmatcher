from crowdrouter import AbstractCrowdRouter, AbstractWorkFlow, AbstractTask
from crowdrouter.decorators import *
from reporting.models import PetReport, PetReportForm
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from utilities.utils import recaptcha_ok, print_info_msg, print_error_msg, print_success_msg, send_email, generate_pet_contacts
from django.contrib import messages
from django.shortcuts import get_object_or_404
from reporting.constants import *
from home.constants import URL_HOME, HTML_HOME
from matching.constants import HTML_MATCHING, HTML_PMDP, URL_PROPOSE_PETMATCH, HTML_PROPOSE_MATCH, UPVOTE, DOWNVOTE, PETMATCH_OUTCOME_UPDATE, PETMATCH_OUTCOME_DUPLICATE_PETMATCH, PETMATCH_OUTCOME_NEW_PETMATCH
from home.models import Activity
from matching.models import PetMatch
from verifying.models import PetMatchCheck
from django.conf import settings
import ipdb

class ReportingTask(AbstractTask):
    @task("/reporting/new")
    def get(self, crowd_request, data, **kwargs):
        return {
            "status": "ok",
            "path": HTML_PETREPORT_FORM,
            "form": PetReportForm(), #Unbound Form
            "RECAPTCHA_CLIENT_SECRET": settings.RECAPTCHA_CLIENT_SECRET,
            "PETREPORT_TAG_INFO_LENGTH":PETREPORT_TAG_INFO_LENGTH,
            "PETREPORT_DESCRIPTION_LENGTH":PETREPORT_DESCRIPTION_LENGTH,
            "PETREPORT_CONTACT_NAME_LENGTH": PETREPORT_CONTACT_NAME_LENGTH,
            "PETREPORT_CONTACT_NUMBER_LENGTH": PETREPORT_CONTACT_NUMBER_LENGTH,
            "PETREPORT_CONTACT_EMAIL_LENGTH": PETREPORT_CONTACT_EMAIL_LENGTH,
            "PETREPORT_CONTACT_LINK_LENGTH": PETREPORT_CONTACT_LINK_LENGTH
        }

    @task("/reporting/submit")
    def post(self, crowd_request, data, form, **kwargs):
        request = self.crowd_request.request_strategy.request
        form = PetReportForm(request.POST, request.FILES)

        if not request.POST["g-recaptcha-response"]:
            messages.error (request, "Please fill in the RECAPTCHA.")
            return {"status":"fail", "form": form, "path": "/reporting/new"}

        if not recaptcha_ok(request.POST["g-recaptcha-response"]):
            messages.error(request, "CAPTCHA was not correct. Please try again.")
            return {"status":"fail", "path": request.path}

        #Let's make some adjustments to non-textual form fields before converting to a PetReportForm.
        geo_lat = request.POST ["geo_location_lat"] or ""
        geo_long = request.POST ["geo_location_long"] or ""

        if (geo_lat == "" or geo_lat == "None") or (geo_long == "" or geo_long == "None"):
            request.POST ['geo_location_lat'] = 0.00
            request.POST ['geo_location_long'] = 0.00
        else:
            request.POST ["geo_location_lat"] = float("%.5f" % float(geo_lat))
            request.POST ["geo_location_long"] = float("%.5f" % float(geo_long))

        if form.is_valid() == True:
            #Create (but do not save) the Pet Report Object associated with this form data.
            pr = form.save(commit=False)
            pr.proposed_by = request.user.userprofile

            #Deal with Contact Information.
            if pr.contact_name.strip() == "":
                pr.contact_name = None
            if pr.contact_email.strip() == "":
                pr.contact_email = None
            if pr.contact_number.strip() == "":
                pr.contact_number = None
            if pr.contact_link.strip() == "":
                pr.contact_link = None

            pr.breed = pr.breed.strip()
            print_info_msg ("Pet Report Image Path: %s" % pr.img_path)

            #Make and save images from img_path and thumb_path AND save the PetReport.
            pr.set_images(pr.img_path, save=True, rotation=request.POST.get("img_rotation"))

            #Add reputation points for submitting a pet report
            request.user.userprofile.update_reputation("ACTIVITY_PETREPORT_SUBMITTED")
            message = "Thank you for your submission. %s %s (%s) is front row on the gallery! " % (pr.status, pr.pet_type, pr.pet_name)
            if pr.status == 'Lost':
                messages.success (request, message + "Your contribution will go a long way towards helping volunteers find your lost pet.")
            else:
                messages.success (request, message + "Your contribution will go a long way towards helping volunteers match your found pet.")

            #Log the PetReport submission for this UserProfile
            Activity.log_activity("ACTIVITY_PETREPORT_SUBMITTED", request.user.userprofile, source=pr)
            print_success_msg("Pet Report submitted successfully")

            #Check to see if there are any matching petreports that have the same microchip ID.
            matching_pet = pr.find_by_microchip_id()
            if matching_pet != None: #Send an email about the match!
                contact1 = generate_pet_contacts(pr)[0]
                contact2 = generate_pet_contacts(matching_pet)[0]
                email_body = render_to_string(EMAIL_BODY_MATCH_BY_MICROCHIP_ID, {
                    "pet": pr,
                    "other_pet": matching_pet,
                    "site": Site.objects.get_current()
                })
                send_email(EMAIL_SUBJECT_MATCH_BY_MICROCHIP_ID, email_body, None, [contact1["email"]])
            return {"path": URL_HOME, "status": "ok"}
        else:
            messages.error(request, "Something went wrong. Please check the fields and try again.")
            print_error_msg ("Pet Report not submitted successfully")
            print_error_msg (form.errors)
            print_error_msg (form.non_field_errors())
            return {
                "status":"fail",
                "path": URL_PETREPORT_FORM,
                "form": form,
                "PETREPORT_TAG_INFO_LENGTH":PETREPORT_TAG_INFO_LENGTH,
                "PETREPORT_DESCRIPTION_LENGTH":PETREPORT_DESCRIPTION_LENGTH,
                "PETREPORT_CONTACT_NAME_LENGTH": PETREPORT_CONTACT_NAME_LENGTH,
                "PETREPORT_CONTACT_NUMBER_LENGTH": PETREPORT_CONTACT_NUMBER_LENGTH,
                "PETREPORT_CONTACT_EMAIL_LENGTH": PETREPORT_CONTACT_EMAIL_LENGTH,
                "PETREPORT_CONTACT_LINK_LENGTH": PETREPORT_CONTACT_LINK_LENGTH
            }

class MatchTask(AbstractTask):
    @task("/matching/new/<petreport_id>")
    def get(self, crowd_request, data, **kwargs):
        petreport_id = self.crowd_request.get_data()["petreport_id"]
        request = self.crowd_request.request_strategy.request
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
            "path": HTML_MATCHING,
            'target_petreport': target_petreport,
            'petreport_fields': target_petreport.get_display_fields(),
            "candidates_count":candidates_count
        }

    @task("/matching/new/<petreport_id>")
    def post(self, crowd_request, data, form, **kwargs):
        target_id = data["petreport_id"]
        candidate_id = form["candidate_id"]
        target = get_object_or_404(PetReport, pk=target_id)
        candidate = get_object_or_404(PetReport, pk=candidate_id)

        if (target.pet_type != candidate.pet_type) or (target.status == candidate.status):
            messages.error(request, "This proposal is invalid! Please try another one.")
            return {"status":"fail", "path": URL_MATCHING + str(target_id)}

        self.crowd_request.request_strategy.data.update({"target_id":target_id, "candidate_id":candidate_id})

        return {
            "status":"ok",
            "path": URL_PROPOSE_PETMATCH + str(target_id) + "/" + str(candidate_id),
            "target_id": target_id,
            "candidate_id": candidate_id
        }

class ProposeMatchTask(AbstractTask):
    @task("/matching/propose/<target_id>/<candidate_id>/")
    def get(self, crowd_request, data, **kwargs):
        target_id = self.crowd_request.get_data()["target_id"]
        candidate_id = self.crowd_request.get_data()["candidate_id"]
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
            "path": HTML_PROPOSE_MATCH,
            "target": target,
            "candidate": candidate,
            "RECAPTCHA_CLIENT_SECRET": settings.RECAPTCHA_CLIENT_SECRET,
            "petreport_fields": petreport_fields
        }

    @task("/matching/propose/<target_id>/<candidate_id>/")
    def post(self, crowd_request, data, form, **kwargs):
        target_id = data["target_id"]
        candidate_id = data["candidate_id"]
        target = get_object_or_404(PetReport, pk=target_id)
        candidate = get_object_or_404(PetReport, pk=candidate_id)
        request = self.crowd_request.request_strategy.request
        proposed_by = request.user.userprofile

        if not request.POST.get("g-recaptcha-response"):
            messages.error(request, "Please Fill in the RECAPTCHA.")
            return {"status":"fail", "path": URL_MATCHING + str(target_id)}

        if not recaptcha_ok(request.POST["g-recaptcha-response"]):
            messages.error(request, "CAPTCHA was not correct. Please try again.")
            return redirect(request.path)

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
        return {"status": "ok", "path": URL_HOME}

class VoteTask(AbstractTask):
    @task("/matching/<petmatch_id>/")
    def get(self, crowd_request, data, **kwargs):
        petmatch_id = data["petmatch_id"]
        request = self.crowd_request.request_strategy.request
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

    @task("/matching/vote/<petmatch_id>")
    def post(self, crowd_request, data, form, **kwargs):
        petmatch_id = data["petmatch_id"]
        vote = form['vote']
        request = self.crowd_request.request_strategy.request
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
            "message": message,
            "threshold_reached": threshold_reached,
            "num_downvotes": num_downvotes,
            "num_upvotes": num_upvotes
        }

class ReportingWorkFlow(AbstractWorkFlow):
    tasks = [ReportingTask]

    def __init__(self, cr):
        self.crowdrouter = cr

    @workflow
    def run(self, task):
        return task.execute()

class MatchingWorkFlow(AbstractWorkFlow):
    tasks = [MatchTask, ProposeMatchTask]

    def __init__(self, cr):
        self.crowdrouter = cr

    @workflow
    def run(self, task):
        return self.pipeline(task)

class VotingWorkFlow(AbstractWorkFlow):
    tasks = [VoteTask]

    def __init__(self, cr):
        self.crowdrouter = cr

    @workflow
    def run(self, task):
        return task.execute()

class EPMCrowdRouter(AbstractCrowdRouter):
    workflows = [ReportingWorkFlow, MatchingWorkFlow, VotingWorkFlow]

    def __init__(self):
        self.enable_crowd_statistics("crowd_stats.db")

    @crowdrouter
    def route(self, crowd_request, workflow):
        return workflow.run(crowd_request)
