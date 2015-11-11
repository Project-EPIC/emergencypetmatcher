from django.db import models
from django import forms
from matching.models import PetMatch
from socializing.models import UserProfile
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from datetime import datetime
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.forms import ModelForm, Textarea
from utilities.utils import *
from home.models import Activity
from home.constants import *
from constants import *
import json, pdb

class PetReunion(models.Model):
	#Required
	petreport = models.OneToOneField("reporting.PetReport", null=False, default=None)
	reason = models.CharField(max_length=PETREUNION_REASON_LENGTH, null=False, default=None)
	#Not Required
	matched_petreport = models.OneToOneField("reporting.PetReport", null=True, default=None, related_name="matched_petreport")
	description = models.CharField(max_length=PETREUNION_DESCRIPTION_LENGTH, null=True, default="")
	img_path = models.ImageField(upload_to=PETREUNION_IMG_PATH, null=True)
	thumb_path = models.ImageField(upload_to=PETREUNION_THUMB_PATH, null=True)

	def get_display_reason(self):
		if "reunited with its original owner" in self.reason:
			return "Reunited"
		elif "rehomed with a new owner" in self.reason:
			return "Rehomed"
		elif "passed away" in self.reason:
			return "RIP"
		return "Closed"

	def get_long_reason(self):
		reason = self.get_display_reason()
		name = self.petreport.pet_name
		if reason == "Reunited":
			return "%s has been reunited with its original owner. Thank you, digital volunteers, for helping %s get back home!" % (name, name)
		elif reason == "Rehomed":
			return "%s has been rehomed with new owners! Thank you, digital volunteers, for helping %s find a new home!" % (name, name)
		elif reason == "RIP":
			return "%s is now resting over the rainbow bridge. Rest in Peace, %s." % (name, name)
		else:
			return "%s has been closed. Thank you digital volunteers for helping %s get back home!" % (name, name)

	def get_display_fields(self):
		return [
			{"attr": "pet_name", "label": "Pet Name", "value": self.petreport.pet_name},
			{"attr": "pet_type", "label": "Pet Type", "value": self.petreport.pet_type},
			{"attr": "reason", "label": "Status", "value": self.reason},
			{"attr": "event_tag", "label":"Event Tag", "value": self.petreport.event_tag},
			{"attr": "location", "label": "Location", "value": self.petreport.location},
			{"attr": "description", "label": "Description", "value": self.description},
		]

	def set_images(self, img_path, save=True, rotation=None):
		if img_path != None:
			img = open_image(img_path) #Safely open the image.

			if save == True:
				self.img_path = None #Save first - we must have the PetReunion ID
				self.save()
				unique_img_name = str(self.id) + "-" + str(self.petreport.id) + ".jpg"

				#Perform rotation (if it applies)
				if rotation != None:
					img = img.rotate(-int(rotation))

				self.img_path = PETREUNION_IMG_PATH + unique_img_name
				self.thumb_path = PETREUNION_THUMB_PATH + unique_img_name
				img.save(PETREUNION_UPLOADS_DIRECTORY + unique_img_name, "JPEG", quality=75)
				img.thumbnail((PETREUNION_THUMBNAIL_WIDTH, PETREUNION_THUMBNAIL_HEIGHT), Image.ANTIALIAS)
				img.save(PETREUNION_THUMBNAILS_DIRECTORY + unique_img_name, "JPEG", quality=75)
				self.save() #Save again.

			else:
				self.img_path = img_path
				self.thumb_path = img_path

		else:
			self.img_path = self.petreport.img_path
			self.thumb_path = self.petreport.thumb_path

		if save == True:
			self.save()

	def to_DICT(self):
		return {
			"id" :self.id,
			"petreport_id": self.petreport.id,
			"petreport_name": self.petreport.pet_name,
			"reason" : self.reason,
			"description": self.description,
			"img_path" : self.img_path.name,
			"thumb_path": self.thumb_path.name
		}

	@staticmethod
	def filter(params, page=1, limit=25):
		for key in params:
			if type(params[key]) == list:
				params[key] = params[key][0]
		params = {k:v for k, v in params.iteritems() if (v != "All" and k != "page")}
		petreunions = PetReunion.objects.filter(**params).order_by("id").reverse()
		count = len(petreunions)
		petreunions = get_objects_by_page(petreunions, page, limit)
		return {"petreunions": petreunions, "count":count}

	def __unicode__ (self):
		return '{ID{%s}, reason:%s, petreport:%s, matched_petreport:%s}' % (self.id, self.reason, self.petreport, self.matched_petreport)



#The PetMatchCheck Model
class PetMatchCheck(models.Model):
	petmatch = models.OneToOneField("matching.PetMatch", null=False, default=None)
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
		return	{
			"id"									: self.id,
			"petmatch"						: self.petmatch.to_DICT(),
			"img_path"            : [self.petmatch.lost_pet.img_path.name, self.petmatch.found_pet.img_path.name],
			"thumb_path"          : [self.petmatch.lost_pet.thumb_path.name, self.petmatch.found_pet.thumb_path.name],
			"verification_votes"	: self.verification_votes
		}

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
		return ("0" not in self.verification_votes)

	def verification_successful(self):
		return self.verification_votes == "11"

	def send_messages_to_contacts(self):
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
				"petmatchcheck_id": self.id,
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
				email_body = render_to_string (TEXTFILE_EMAIL_CROSSPOSTER_VERIFY_PETMATCH, {"site":site, "pet": pet, "petmatchcheck_id":self.id, "petmatch": petmatch})
				send_mail(email_subject, email_body, None, [cc["email"]])

			ctx = {
				"site": site,
				"pet": pet,
				"petmatcher": petmatch_owner,
				"petmatch": petmatch,
				"petmatchcheck_id": self.id,
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

	def close_PetMatch(self):
		petmatch = self.petmatch
		petmatch_owner = petmatch.proposed_by
		lost_pet = petmatch.lost_pet
		lost_pet_contact = lost_pet.proposed_by
		found_pet = petmatch.found_pet
		found_pet_contact = found_pet.proposed_by
		self.closed_date = datetime.now()

		if self.verification_successful() == True:
			successful = True
			self.is_successful = True
			lost_pet.closed = True
			found_pet.closed = True
			self.save()
			lost_pet.save()
			found_pet.save()

			Activity.log_activity("ACTIVITY_PETMATCHCHECK_VERIFY_SUCCESS", lost_pet_contact, source=self)
			lost_pet_contact.update_reputation("ACTIVITY_PETMATCHCHECK_VERIFY_SUCCESS")
			Activity.log_activity("ACTIVITY_PETMATCHCHECK_VERIFY_SUCCESS", found_pet_contact, source=self)
			found_pet_contact.update_reputation("ACTIVITY_PETMATCHCHECK_VERIFY_SUCCESS")

			#Check if the petmatch owner is somebody different - if so, log and award him/her points too.
			if petmatch_owner.id not in [lost_pet_contact.id, found_pet_contact.id]:
				Activity.log_activity("ACTIVITY_PETMATCHCHECK_VERIFY_SUCCESS", petmatch_owner, source=self)
				petmatch_owner.update_reputation("ACTIVITY_PETMATCHCHECK_VERIFY_SUCCESS")
			print_info_msg ("PetMatch %s is now closed" % (self))

		#If not successful, delete the PetMatchCheck object, award pet points, and notify.
		else:
			successful = False
			petmatch.has_failed = True
			Activity.log_activity("ACTIVITY_PETMATCHCHECK_VERIFY_FAIL", lost_pet_contact, source=self)
			Activity.log_activity("ACTIVITY_PETMATCHCHECK_VERIFY_FAIL", found_pet_contact, source=self)
			found_pet_contact.update_reputation("ACTIVITY_PETMATCHCHECK_VERIFY_FAIL")
			lost_pet_contact.update_reputation("ACTIVITY_PETMATCHCHECK_VERIFY_FAIL")

			#Check if the petmatch owner is somebody different - if so, log and award him/her points too.
			if petmatch_owner.id not in [lost_pet_contact.id, found_pet_contact.id]:
				Activity.log_activity("ACTIVITY_PETMATCHCHECK_VERIFY_FAIL", petmatch_owner, source=self)
				petmatch_owner.update_reputation("ACTIVITY_PETMATCHCHECK_VERIFY_FAIL")

			print_info_msg ("PetMatch %s did not pass verification!" % (self))
			del self

		petmatch.save()
		return successful

	def __unicode__ (self):
		return '{ID{%s} petmatch:%s, votes:%s}' % (self.id, self.petmatch, self.verification_votes)


#The PetReunion ModelForm
class PetReunionForm (ModelForm):
	reason 	= forms.CharField(label="Reason for Closing", max_length=PETREUNION_REASON_LENGTH, required=True, widget=forms.Select(attrs={"style":"width:300px; display:block;"}))
	description = forms.CharField(label='Description', max_length=PETREUNION_DESCRIPTION_LENGTH, required=False, widget=forms.Textarea(attrs={"class":"form-control", "placeholder": "(Please provide more information on why this pet report is being closed)", "style":"max-width:400px; max-height:150px;"}))
	img_path = forms.ImageField(label="Upload an Image", help_text="(*.jpg, *.png, *.bmp), 3MB maximum", required = False, widget=forms.FileInput)

	class Meta:
		model = PetReunion
		fields = ("reason", "description", "img_path")


#Create a post save signal function to setup a PetReunion when it is created
@receiver (post_save, sender=PetReunion)
def setup_PetReunion(sender, instance, created, **kwargs):
	if created == True:
		userprofile = instance.petreport.proposed_by
		instance.petreport.closed = True
		instance.petreport.save()

		if instance.matched_petreport:
			instance.matched_petreport.closed = True
			instance.matched_petreport.save()

		Activity.log_activity("ACTIVITY_PETREUNION_CREATED", userprofile, source=instance)
		userprofile.update_reputation("ACTIVITY_PETREUNION_CREATED")
