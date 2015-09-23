from django.db import models
from matching.models import PetMatch
from socializing.models import UserProfile
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from datetime import datetime
from utilities.utils import *
from home.models import Activity
from home.constants import *
from constants import *
import json, pdb

#The Pet Check Model
class PetCheck(models.Model):
	petmatch = models.OneToOneField("matching.PetMatch", null=True, default=None)
	is_successful = models.BooleanField(default=False)
	#closed_date is the date when the PetMatch is closed for good (after verification)
	closed_date = models.DateTimeField(null=True)
	#verification_votes represents user responses sent via the verify_petmatch webpage.
	#the first bit holds the Lost Contact's response and the second bit holds the 
	#Found Contact's response. 
	#0 - No response was recorded
	#1 - user clicked on Yes
	#2 - User clicked on No
	verification_votes = models.CharField(max_length=2, default='00')


	def to_DICT(self):
		return	{	"id"									: self.id,
							"petmatch"						: self.petmatch.to_DICT(),
							"img_path"            : [self.petmatch.lost_pet.img_path.name, self.petmatch.found_pet.img_path.name],
							"thumb_path"          : [self.petmatch.lost_pet.thumb_path.name, self.petmatch.found_pet.thumb_path.name],
							"verification_votes"	: self.verification_votes }

	def to_JSON(self):
		return json.dumps(self.to_DICT())

	def UserProfile_has_verified(self, profile):
		if profile == self.petmatch.lost_pet.proposed_by:
			pos = 0
		elif profile == self.petmatch.found_pet.proposed_by:
			pos = 1
		else:
			return False
		return self.verification_votes[pos] in ["1","2"]

	def verification_complete(self):
		return "0" not in self.verification_votes

	def verification_successful(self):
		return self.verification_votes == "11"

	def verify_PetMatch(self):
		print_info_msg("Pet Checking Triggered: PetMatch is now closed to the crowd.")
		petmatch = self.petmatch
		lost_pet = petmatch.lost_pet
		found_pet = petmatch.found_pet
		petmatch_owner = petmatch.proposed_by
		site = Site.objects.get_current()

		#Craft the message that you'll send back to pet contacts.
		# (oc = original contact, cc = crossposting contact)
		lost_oc, lost_cc = generate_pet_contacts(lost_pet)
		found_oc, found_cc = generate_pet_contacts(found_pet)
		send_petmatch_email = True
		email_subject = EMAIL_SUBJECT_VERIFY_PETMATCH
		message = "Congratulations - These two pets are ready to be checked by their contacts! All votes are closed. Thanks for voting!"

		#Send the verify email to the petmatch proposer (if different from the original or crossposting contacts)
		if lost_cc:
			if petmatch.proposed_by.user.email in lost_cc["email"]:
				send_petmatch_email = False 
		if found_cc:
			if petmatch.proposed_by.user.email in found_cc["email"]:
				send_petmatch_email = False 
		if petmatch.proposed_by.user.email in (lost_oc["email"], found_oc["email"]):
			send_petmatch_email = False

		if send_petmatch_email == True:
			email_body = render_to_string(TEXTFILE_EMAIL_MATCHER_VERIFY_PETMATCH, { 
				"site": site,
				"lost_pet": lost_pet,
				"found_pet": found_pet,
				"petcheck_id": self.id,
				"petmatch": petmatch 
			})
			send_mail(email_subject, email_body, None, [petmatch_owner.user.email])

		#Iterate through lost and found original and crossposting contacts and email them accordingly. Do this smartly.
		for (oc, cc, pet, other_oc, other_cc, other_pet) in ((lost_oc, lost_cc, lost_pet, found_oc, found_cc, found_pet), 
			(found_oc, found_cc, found_pet, lost_oc, lost_cc, lost_pet)):
		
			cross_posting_phrase = ""
			cross_posting_reach_out = ""

			#We have a crossposter EPM user.
			if cc != None:
				cross_posting_phrase = "- A volunteer with username %s has posted your pet on EPM on your behalf, thereby making the match possible." % (cc["name"])
				cross_posting_reach_out = "Please include %s at %s in your conversations, since this person will make the decision on EPM on your behalf." % (cc["name"], cc["email"])
				email_body = render_to_string (TEXTFILE_EMAIL_CROSSPOSTER_VERIFY_PETMATCH, {"site":site, "pet": pet, "petcheck_id":self.id, "petmatch": petmatch})
				send_mail(email_subject, email_body, None, [cc["email"]])

			ctx = {
				"site": site, 
				"pet": pet,
				"petmatcher": petmatch_owner,
				"petmatch": petmatch, 
				"petcheck_id": self.id,
				"cross_posting_phrase": cross_posting_phrase,
				"cross_posting_reach_out": cross_posting_reach_out,
				"other_contact": other_oc,
				"other_pet": other_pet 			
			}

			if other_cc:
				ctx["other_contact"] = other_cc 

			email_body = render_to_string (TEXTFILE_EMAIL_PETOWNER_VERIFY_PETMATCH, ctx)
			
			#Setup guardian as CC'ed on this email.
			if oc.get("guardian_email"):
				email_cc = [oc["guardian_email"]]
			else:
				email_cc = None
				
			email_message = EmailMessage(email_subject, email_body, to=[oc["email"]], cc=email_cc)
			email_message.send(fail_silently=True)
		return message

	#This function will either set the PetMatch to its successful state, whereupon it will be galleried; 
	#or, it will be set back to its unsuccessful state, and the petcheck object will be removed.
	#If successful, the function will remove any other petmatches associated with these pet reports.
	def close_PetMatch(self):
		petmatch = self.petmatch
		petmatch_owner = petmatch.proposed_by
		lost_pet = petmatch.lost_pet
		lost_pet_contact = lost_pet.proposed_by
		found_pet = petmatch.found_pet
		found_pet_contact = found_pet.proposed_by
		self.closed_date = datetime.now()

		#If successful, trigger the success parameters and award pet points to those involved.
		if self.verification_successful() == True:
			self.is_successful = True	
			petmatch.is_successful = True
			lost_pet.closed = True
			found_pet.closed = True
			self.save()    
			lost_pet.save()
			found_pet.save()
			message = "Thanks for your response, and congratulations on the successful match! You have earned %s Pet Points. The reunited match can be found in the 'Reunited Pets' Tab." % ACTIVITIES["ACTIVITY_PETCHECK_VERIFY_SUCCESS"]["reward"]

			if lost_pet.UserProfile_is_owner(lost_pet_contact) == True:
				Activity.log_activity("ACTIVITY_PETCHECK_VERIFY_SUCCESS_OWNER", lost_pet_contact, source=self)			
				lost_pet_contact.update_reputation("ACTIVITY_PETCHECK_VERIFY_SUCCESS_OWNER")
			else:
				Activity.log_activity("ACTIVITY_PETCHECK_VERIFY_SUCCESS", lost_pet_contact, source=self)			
				lost_pet_contact.update_reputation("ACTIVITY_PETCHECK_VERIFY_SUCCESS")

			Activity.log_activity("ACTIVITY_PETCHECK_VERIFY_SUCCESS", found_pet_contact, source=self)
			found_pet_contact.update_reputation("ACTIVITY_PETCHECK_VERIFY_SUCCESS")

			#Check if the petmatch owner is somebody different - if so, log and award him/her points too.
			if petmatch_owner.id not in [lost_pet_contact.id, found_pet_contact.id]:				
				Activity.log_activity("ACTIVITY_PETCHECK_VERIFY_SUCCESS", petmatch_owner, source=self)
				petmatch_owner.update_reputation("ACTIVITY_PETCHECK_VERIFY_SUCCESS")

			print_info_msg ("PetMatch %s is now closed" % (self))

		#If not successful, delete the PetCheck object, award pet points, and notify.
		else:
			message = "Unfortunately, this Pet Match was not successful. The pet contacts have agreed that this wasn't the right match. You have earned %d Pet Points. Please try other matches!" % ACTIVITIES["ACTIVITY_PETCHECK_VERIFY_FAIL"]["reward"]
			petmatch.has_failed = True
			Activity.log_activity("ACTIVITY_PETCHECK_VERIFY_FAIL", lost_pet_contact, source=self)
			Activity.log_activity("ACTIVITY_PETCHECK_VERIFY_FAIL", found_pet_contact, source=self)	
			found_pet_contact.update_reputation("ACTIVITY_PETCHECK_VERIFY_FAIL")
			lost_pet_contact.update_reputation("ACTIVITY_PETCHECK_VERIFY_FAIL")

			#Check if the petmatch owner is somebody different - if so, log and award him/her points too.
			if petmatch_owner.id not in [lost_pet_contact.id, found_pet_contact.id]:
				Activity.log_activity("ACTIVITY_PETCHECK_VERIFY_FAIL", petmatch_owner, source=self)
				petmatch_owner.update_reputation("ACTIVITY_PETCHECK_VERIFY_FAIL")			

			print_info_msg ("PetMatch %s did not pass verification!" % (self))
			del self

		petmatch.save()	
		return message

	def __unicode__ (self):
		return '{ID{%s} petmatch:%s, votes:%s}' % (self.id, self.petmatch, self.verification_votes)





