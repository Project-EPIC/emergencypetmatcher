from django.db import models
from matching.models import PetMatch
from social.models import UserProfile
from django.contrib.sites.models import Site
from utilities.utils import *
from constants import *

#The Pet Check Model
class PetCheck(models.Model):
	petmatch = models.OneToOneField(PetMatch, null=False, default=None)
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

    def verify_PetMatch(self):
    	print_info_msg("Verification Triggered: PetMatch is now closed to the crowd.")
    	petmatch = self.petmatch
    	lost_pet = petmatch.lost_pet
    	found_pet = petmatch.found_pet
    	petmatch_owner = petmatch.proposed_by
    	site = Site.objects.get_current()

    	#Craft the message that you'll send back to receiver (voting on PetMatch view)
    	message = "Congratulations - These two pets have now been triggered for verification! All votes are closed."        

    	#Crossposted will tell us whether or not there exist contact preferences.
    	lost_pet_crossposted = False
    	found_pet_crossposted = False

    	#LOST PET CONTACT: We might have contact preferences, so we need to use their emails (only if available).
    	if (lost_pet.contact_email or lost_pet.contact_name or lost_pet.contact_number or lost_pet.contact_link):
    		lost_pet_contact = {"name":lost_pet.contact_name, 
    							"email": lost_pet.contact_email, 
    							"phone": lost_pet.contact_number, 
    							"link": lost_pet.contact_link, 
    							"crossposted":True}

    	#Just use the lost pet contact.
    	else:
    		lost_pet_contact = {"name": lost_pet.proposed_by.user.username, 
    							"email":lost_pet.proposed_by.user.email, 
    							"phone":None, 
    							"link":None, 
    							"crossposted":False }

	        #FOUND PET CONTACT: We might have contact preferences, so we need to use their emails (only if available).
	        if (found_pet.contact_email or found_pet.contact_name or found_pet.contact_number or found_pet.contact_link):
	            found_pet_contact = {"name":found_pet.contact_name, "email": found_pet.contact_email, "phone": found_pet.contact_number, "link":found_pet.contact_link}
	            found_pet_contact_name = found_pet_contact.get("name") or "the other contact (we do not have his/her name on file)"
	            found_pet_contact_email = found_pet_contact.get("email")
	            found_pet_contact_phone = found_pet_contact.get("phone")
	            found_pet_crossposted = True

	        #Just use the found pet contact.                        
	        else:
	            found_pet_contact = found_pet.proposed_by
	            found_pet_contact_name = found_pet_contact.user.username
	            found_pet_contact_email = found_pet_contact.user.email
	            found_pet_contact_phone = None

	        #By default, the petmatch proposer should be involved in the pet match verification discussion.
	        optionally_discuss_with_digital_volunteer = " You may also discuss this pet match with %s (%s), the digital volunteer who proposed this pet match." % (petmatch_owner.user.username, petmatch_owner.user.email)

	        #But if the PetMatch proposer is either the lost or found pet contact...
	        if (lost_pet_crossposted == False and found_pet_crossposted == False) and ((petmatch_owner.id == lost_pet_contact.id) or (petmatch_owner.id == found_pet_contact.id)):
	            optionally_discuss_with_digital_volunteer = ""
	        
	        #Create email for regular or crossposted lost pet contact.
	        if lost_pet_contact_email and validate_email(lost_pet_contact_email):

	            #How to reach the opposite contact.
	            if found_pet_contact_email != None:
	                ability_to_reach_opposite_contact = "You can reach him/her at %s" % found_pet_contact_email
	            elif found_pet_contact_phone != None:
	                ability_to_reach_opposite_contact = "Since no email is given for this contact, you can reach him/her at: %s" % found_pet_contact_phone
	            else:
	                ability_to_reach_opposite_contact =  "Unfortunately, there is no information to use to reach this contact, but if you help share this PetMatch online, more people can help trace him/her back."  

	            #Reaching Verification Page (when not crossposted).
	            if lost_pet_crossposted == False:
	                verification_page = "http://%s%s" % (site.domain, URL_VERIFY_PETMATCH + str(self.id))
	                access_verification = "Please let us know if this pet match was successful by visiting the following link: %s" % verification_page
	            else:
	                access_verification = ""

	            ctx = { "site": site,
	                    "petmatch_id": self.id,
	                    "pet_type": "your lost pet",
	                    "opposite_pet_type_contact_name": found_pet_contact_name,
	                    "pet_status": "found",
	                    "ability_to_reach_opposite_contact": ability_to_reach_opposite_contact,
	                    "optionally_discuss_with_digital_volunteer": optionally_discuss_with_digital_volunteer,
	                    "access_verification": access_verification }

	            email_body = render_to_string(TEXTFILE_EMAIL_PETOWNER_VERIFY_PETMATCH, ctx)
	            email_subject = EMAIL_SUBJECT_PETOWNER_VERIFY_PETMATCH
	            send_mail(email_subject, email_body, None,[lost_pet_contact_email])

	        #Create email for regular or crossposted found pet contact.
	        if found_pet_contact_email and validate_email(found_pet_contact_email):

	            #How to reach the opposite contact.
	            if lost_pet_contact_email != None:
	                ability_to_reach_opposite_contact = "You can reach him/her at %s" % lost_pet_contact_email
	            elif lost_pet_contact_phone != None:
	                ability_to_reach_opposite_contact = "Since no email is given for this contact, you can reach him/her at: %s" % lost_pet_contact_phone
	            else:
	                ability_to_reach_opposite_contact =  "Unfortunately, there is no information to use to reach this contact, but if you help share this PetMatch online, more people can help trace him/her back."  

	            #Reaching Verification Page (when not crossposted).
	            if found_pet_crossposted == False:
	                verification_page = "http://%s%s" % (site.domain, URL_VERIFY_PETMATCH + str(self.id))
	                access_verification = "Please let us know if this pet match was successful by visiting the following link: %s" % verification_page
	            else:
	                access_verification = ""

	            ctx = { "site": site,
	                    "petmatch_id": self.id,
	                    "pet_type": "the pet you found",
	                    "opposite_pet_type_contact_name": lost_pet_contact_name,
	                    "pet_status": "lost",
	                    "ability_to_reach_opposite_contact": ability_to_reach_opposite_contact,
	                    "optionally_discuss_with_digital_volunteer": optionally_discuss_with_digital_volunteer,
	                    "access_verification": access_verification }

	            email_body = render_to_string(TEXTFILE_EMAIL_PETOWNER_VERIFY_PETMATCH, ctx)
	            email_subject = EMAIL_SUBJECT_PETOWNER_VERIFY_PETMATCH
	            send_mail(email_subject, email_body, None, [found_pet_contact_email], ctx)

	        #If the lost/found pet contact emails exist, then add that emails have been sent.
	        if lost_pet_contact_email != None and found_pet_contact_email != None:
	            message = message + " Emails have been sent to the original contacts of these pets."
	        else:
	            message = message + " Help us get in contact with the original owners about this potential match by sharing it!"


	        #If the pet match was proposed by a person other than the lost_pet_contact/found_pet_contact, an email will be sent to this person as well.
	        if optionally_discuss_with_digital_volunteer != "" and validate_email(petmatch_owner.user.email):

	            #If at least one pet contact is being crossposted, mention that pet match proposer is responsible for managing yes/no for that contact.
	            if lost_pet_crossposted == True or found_pet_crossposted == True:
	                manage_answer = "Since at least one pet contact is not on EmergencyPetMatcher, we are relying on you and the EPM users who submitted these pets to acquire the responses from the original pet owner and finder. Please work together and communicate a final response for this pet!"
	            else:
	                manage_answer = ""

	            #How to reach lost pet contact.
	            if lost_pet_contact_email != None:
	                reach_lost_pet_contact = "You can reach him/her at %s" % lost_pet_contact_email
	            elif lost_pet_contact_phone != None:
	                reach_lost_pet_contact = "Since no email is given for this contact, you can reach him/her at: %s" % lost_pet_contact_phone
	            else:
	                reach_lost_pet_contact =  "Unfortunately, there is no information to use to reach this contact, but if you help share this PetMatch online, more people can help trace him/her back."  

	            #How to reach found pet contact.
	            if found_pet_contact_email != None:
	                reach_found_pet_contact = "You can reach him/her at %s" % found_pet_contact_email
	            elif found_pet_contact_phone != None:
	                reach_found_pet_contact = "Since no email is given for this contact, you can reach him/her at: %s" % found_pet_contact_phone
	            else:
	                reach_found_pet_contact =  "Unfortunately, there is no information to use to reach this contact, but if you help share this PetMatch online, more people can help trace him/her back."  

	            #Reaching Verification Page (when not crossposted).
	            if petmatch_owner.id == lost_pet.proposed_by.id or petmatch_owner.id == found_pet.proposed_by.id:
	                verification_page = "http://%s%s" % (site.domain, URL_VERIFY_PETMATCH + str(self.id))
	                access_verification = "Please let us know if this pet match was successful by visiting the following link: %s" % verification_page
	            else:
	                access_verification = ""


	            ctx = { "site": site,
	                    "petmatch_id": self.id,
	                    'lost_pet_contact_name':lost_pet_contact_name,
	                    'reach_lost_pet_contact':reach_lost_pet_contact,
	                    'found_pet_contact_name':found_pet_contact_name,
	                    'reach_found_pet_contact':reach_found_pet_contact,
	                    "access_verification": access_verification,
	                    "manage_answer": manage_answer }

	            email_body = render_to_string(TEXTFILE_EMAIL_PETMATCH_PROPOSER, ctx)
	            email_subject =  EMAIL_SUBJECT_PETMATCH_PROPOSER  
	            send_mail (email_subject, email_body, None, [petmatch_owner.user.email])

	        #Save after successfully sending off pet contact emails.
	        self.save()
	        return message
	            
	    def close_PetMatch(self):
	        petmatch_owner = self.proposed_by
	        lost_pet_contact = self.lost_pet.proposed_by
	        found_pet_contact = self.found_pet.proposed_by

	        if '0' not in self.verification_votes:
	            self.closed_date = datetime_now()

	            #If the PetMatch is successful, all related PetMatches will be closed and is_successful is set to True.
	            if self.verification_votes == '11':
	                self.is_successful = True

	                for petmatch in self.lost_pet.lost_pet_related.all(): 
	                    petmatch.is_open = False
	                    petmatch.closed_date = datetime_now()
	                    petmatch.save()
	                for petmatch in self.found_pet.found_pet_related.all():
	                    petmatch.is_open = False
	                    petmatch.closed_date = datetime_now()
	                    petmatch.save()

	                #the lost and found pet reports for the pet match are closed
	                petmatch.lost_pet.closed = True
	                petmatch.lost_pet.save()
	                petmatch.found_pet.closed = True
	                petmatch.found_pet.save()
	                
	                # --------Reputation points--------
	                # update reputation points for the following users:
	                # petmatch_owner, lost_pet_contact, and found_pet_contact
	                print_info_msg ("PetMatch Verification for %s was a SUCCESS!" % self)

	                # Must to update reputation points twice since if updating petmatch_owner and lost_pet_contact
	                # separately for the same user doesn't work
	                if petmatch_owner.id == lost_pet_contact.id:
	                    petmatch_owner.update_reputation(ACTIVITY_USER_PROPOSED_PETMATCH_SUCCESSFUL)
	                    petmatch_owner.update_reputation(ACTIVITY_USER_VERIFY_PETMATCH_SUCCESSFUL)
	                    found_pet_contact.update_reputation(ACTIVITY_USER_VERIFY_PETMATCH_SUCCESSFUL)

	                # Must to update reputation points twice since if updating petmatch_owner and found_pet_contact
	                # separately for the same user doesn't work
	                elif petmatch_owner.id == found_pet_contact.id:
	                    petmatch_owner.update_reputation(ACTIVITY_USER_PROPOSED_PETMATCH_SUCCESSFUL)
	                    petmatch_owner.update_reputation(ACTIVITY_USER_VERIFY_PETMATCH_SUCCESSFUL)
	                    lost_pet_contact.update_reputation(ACTIVITY_USER_VERIFY_PETMATCH_SUCCESSFUL)

	                else:
	                    petmatch_owner.update_reputation(ACTIVITY_USER_PROPOSED_PETMATCH_SUCCESSFUL)
	                    lost_pet_contact.update_reputation(ACTIVITY_USER_VERIFY_PETMATCH_SUCCESSFUL)
	                    found_pet_contact.update_reputation(ACTIVITY_USER_VERIFY_PETMATCH_SUCCESSFUL)

	                 # update reputation points for upvoters
	                for upvoters in self.up_votes.all():
	                    upvoters.update_reputation(ACTIVITY_PETMATCH_UPVOTE_SUCCESSFUL)

	                # Must update reputation manually for petmatch_owner if found in the up_votes list because
	                # the user is not updated in the previous for loop
	                if petmatch_owner in self.up_votes.all():
	                    petmatch_owner.update_reputation(ACTIVITY_PETMATCH_UPVOTE_SUCCESSFUL)

	                # Must update reputation manually for lost_pet_contact if found in the up_votes list because
	                # the user is not updated in the previous for loop
	                elif lost_pet_contact in self.up_votes.all():
	                    lost_pet_contact.update_reputation(ACTIVITY_PETMATCH_UPVOTE_SUCCESSFUL)

	                # Must update reputation manually for ound_pet_contact if found in the up_votes list because
	                # the user is not updated in the previous for loop
	                elif found_pet_contact in self.up_votes.all():
	                    found_pet_contact.update_reputation(ACTIVITY_PETMATCH_UPVOTE_SUCCESSFUL)

	                message = "Thanks for your response, and congratulations on the successful match! The reunited match can be found in the 'Reunited Pets' Tab."

	            else: 
	                print_info_msg ("PetMatch Verification for %s was NOT a success!" % self) 
	                message = "Thanks for your response. Unfortunately, the match wasn't a success. Keep trying and don't give up!"
	                petmatch_owner.update_reputation(ACTIVITY_USER_PROPOSED_PETMATCH_FAILURE)

	            self.save()    
	            print_info_msg ("PetMatch %s is now closed" % (self))
	            return message    

