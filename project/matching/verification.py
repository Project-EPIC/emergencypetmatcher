# from constants import *
from home.models import UserProfile, PetReport, PetMatch,User
from django.template.loader import render_to_string
'''===================================================================================
[verification.py]: PetMatch verification Functionality for the EPM system
==================================================================================='''
def verify_pet_match(pet_match):

	petmatch_owner = pet_match.proposed_by.user
	lost_pet_contact = pet_match.lost_pet.proposed_by.user
	found_pet_contact = pet_match.found_pet.proposed_by.user

	Optionally_discuss_with_digital_volunteer = "You may also discuss this pet match with %s, the digital volunteer who proposed this pet match. You can reach %s at %s" % (pet_match.proposed_by.user.username,pet_match.proposed_by.user.username,pet_match.proposed_by.user.email)
	email_petmatch_owner = True

    #An email is sent to the lost pet owner
    ctx = {'pet_type':'your lost pet','opposite_pet_type_contact':found_pet_contact,'pet_status':"found",'Optionally_discuss_with_digital_volunteer':Optionally_discuss_with_digital_volunteer}
	email_body = render_to_string('/srv/epm/static/templates/matching/verification_email_to_pet_owner.txt',ctx)
    email_subject = "We have a found a potential match for your pet!"
    #lost_pet_contact.email_user(email_subject,email_body,from_email=None)
    print 'email to lost pet owner: '+email_body
    
    ''' An email is sent to the lost pet owner '''
    ctx = {'pet_type':'the pet you found','opposite_pet_type_contact':lost_pet_contact,'pet_status':"lost",'Optionally_discuss_with_digital_volunteer':Optionally_discuss_with_digital_volunteer}
    email_body = render_to_string('/srv/epm/static/templates/matching/verification_email_to_pet_owner.txt',ctx)
    email_subject = "We have a found a potential match for your pet!"
    #found_pet_contact.email_user(email_subject,email_body,from_email=None)
    print 'email to found pet owner: '+email_body
   
    '''If the pet match was proposed by a person other than the lost_pet_contact/found_pet_contact,
    an email will be sent to this person '''
    ctx = { 'lost_pet_contact':lost_pet_contact,'found_pet_contact':found_pet_contact }
	email_body = render_to_string('/srv/epm/static/templates/matching/verification_email_to_digital_volunteer.txt',ctx)
	email_subject = 'Your pet match is close to being successful!'    
	#petmatch_owner.email_user(email_subject,email_body,from_email=None)
	print 'email to pet match owner: '+email_body
 #    if petmatch_owner.username == lost_pet_contact.username:
 #    	Optionally_discuss_with_digital_volunteer = ""
 #        email_petmatch_owner = False
 # #    else: