import os, django
django.setup()
os.environ['DJANGO_SETTINGS_MODULE']='project.settings'
from django.test.client import Client
from django.conf import settings
from registration.models import RegistrationProfile
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from home.models import Activity
from socializing.models import UserProfile, UserProfileForm, EditUserProfile
from reporting.models import PetReport, PetReportForm
from matching.models import PetMatch
from verifying.models import PetCheck
from social.apps.django_app.default.models import UserSocialAuth
from django.db import IntegrityError
from random import randint
from datetime import datetime
from home.constants import *
from socializing.constants import *
from reporting.constants import *
from matching.constants import *
from verifying.constants import *
from utilities.utils import *
from pprint import pprint
import random, string, sys, time, datetime, lipsum, traceback

#Control Variables
NUM_PETREPORTS = 200
NUM_USERS = 20
NUM_PETMATCHES = 20
	
#=================================# Functions #=================================#

#Delete all model, user-uploaded, and activity data
def delete_all(leave_Users = True):
	#Delete Model data.
	PetMatch.objects.all().delete()
	PetReport.objects.all().delete()
	delete_PetReport_images()
	Activity.objects.all().delete()

	if leave_Users == False:
		User.objects.all().delete()
		EditUserProfile.objects.all().delete()
		RegistrationProfile.objects.all().delete()
		UserSocialAuth.objects.all().delete()
		delete_UserProfile_images()

#Deletes all images in the designated folder
def delete_images(target_dir=None, from_list=None):
	for the_file in os.listdir(target_dir):
		file_path = os.path.join(target_dir, the_file)
		try:
			if from_list != None:
				if os.path.isfile(file_path) and the_file in from_list:
					os.unlink(file_path)
					print_info_msg ("Removed %s" % the_file)
			else:
				if os.path.isfile(file_path):
					os.unlink(file_path)

		except Exception as e:
			print_error_msg ("Problem in delete_images(): {%s}" % e)
			return False

	if from_list != None:
		print_success_msg ("Specified Files in '%s' are now deleted." % target_dir)
	else:
		print_success_msg("All Files in '%s' are now deleted." % target_dir)


#Overloaded function for deleting PetReport images and thumbnails.
def delete_PetReport_images():
	delete_images(target_dir=PETREPORT_UPLOADS_DIRECTORY)
	delete_images(target_dir=PETREPORT_THUMBNAILS_DIRECTORY)

#Overloaded function for deleting UserProfile images and thumbnails.
def delete_UserProfile_images():
	delete_images(target_dir=USERPROFILE_UPLOADS_DIRECTORY)
	delete_images(target_dir=USERPROFILE_THUMBNAILS_DIRECTORY)

#Create Random Object for: User
def create_random_User(i, pretty_name=True):
	if pretty_name == True:
		username = random.choice(USER_NAMES) + str(i)
	else:
		username = generate_string(10) + str(i)

	#To prevent duplicate usernames
	while(UserProfile.username_exists(username)):
		if pretty_name == True:
			username = random.choice(USER_NAMES) + str(i)
		else:
			username = generate_string(10) + str(i)

	password = generate_string(10)
	email = generate_string(6) + '(at)' + 'test.com'

	try:
		user = User.objects.create_user(username = username, email = email, password = password)
	except IntegrityError, e:
		print_error_msg (str(e.message))

	userprofile = user.userprofile
	return (user, password)

#returns a random list of UserProfiles
def create_random_Userlist(num_users = None): 
	allusers = UserProfile.objects.all()

	if num_users == None:
		num_users = random.randint(0, len(allusers))

	userlist = random.sample(allusers,num_users)
	return userlist

#creates a list of UserProfiles being followed by the input UserProfile
def create_random_following_list (userprofile, num_following=None):
	allusers = UserProfile.objects.exclude(pk = userprofile.user.id)

	#Remember to initialize this list first before adding.
	userprofile.following = []

	if num_following == None:
		num_following = random.randint(0, len(allusers)/2)

	following_list = random.sample(allusers, num_following)

	for followed in following_list:
		userprofile.following.add(followed)
		Activity.log_activity("ACTIVITY_SOCIAL_FOLLOW", userprofile, followed)

	print_success_msg("following list created for %s" % userprofile)
	return userprofile

#creates a list of PetReports being bookmarked by the input UserProfile
def create_random_bookmark_list (userprofile, num_bookmark=None):
	allpetreports = PetReport.objects.all()

	#Remember to initialize this list before adding.
	userprofile.bookmarks_related = []

	if num_bookmark == None:
		num_bookmark = random.randint(0, len(allpetreports))

	bookmark_list = random.sample(allpetreports, num_bookmark)

	for bookmark in bookmark_list:
		userprofile.bookmarks_related.add(bookmark)

	print_success_msg("bookmark list created for %s" % userprofile)
	return userprofile

#Create Random Object for: PetReport
def create_random_PetReport(save=True, user=None, status=None, pet_type=None):
	#Bias the distribution towards (in order): [Dog, Cat, Bird, Horse, Rabbit, Snake, Turtle]
	if pet_type == None:
		random_var = random.random()
		if random_var < 0.60:
			pet_type = PETREPORT_PET_TYPE_DOG
		elif random_var >= 0.60 and random_var < 0.93:
			pet_type = PETREPORT_PET_TYPE_CAT
		elif random_var >= 0.93 and random_var < 0.95:
			pet_type = PETREPORT_PET_TYPE_BIRD
		elif random_var >= 0.95 and random_var < 0.97:
			pet_type = PETREPORT_PET_TYPE_HORSE
		elif random_var >= 0.97 and random_var < 0.98:
			pet_type = PETREPORT_PET_TYPE_RABBIT
		elif random_var >= 0.98 and random_var < 0.99:
			pet_type = PETREPORT_PET_TYPE_SNAKE
		elif random_var >= 0.99 and random_var < 0.995:
			pet_type = PETREPORT_PET_TYPE_TURTLE
		else:
			pet_type = PETREPORT_PET_TYPE_OTHER

	if status == None:
		status = random.choice(STATUS_CHOICES)[0]
	if user == None:
		user = random.choice(User.objects.all())

	#Populate the PetReport with the required fields.
	pr = PetReport (pet_type = pet_type, status = status, proposed_by = user.userprofile)
	pr.date_lost_or_found = generate_random_date(DATE_LOWER_BOUND, DATE_UPPER_BOUND, "%Y-%m-%d", random.random())
	pr.sex = random.choice(SEX_CHOICES)[0]
	pr.size = random.choice(SIZE_CHOICES)[0] 
	pr.location = generate_string(PETREPORT_LOCATION_LENGTH) 
	pr.color = generate_string(PETREPORT_COLOR_LENGTH)
	pr.age = random.choice(AGE_CHOICES)[0]

	#Load breeds in memory.
	breeds = {
		PETREPORT_PET_TYPE_DOG: PetReport.get_pet_breeds(PETREPORT_PET_TYPE_DOG),
	  PETREPORT_PET_TYPE_CAT: PetReport.get_pet_breeds(PETREPORT_PET_TYPE_CAT),
	 	PETREPORT_PET_TYPE_HORSE: PetReport.get_pet_breeds(PETREPORT_PET_TYPE_HORSE),
	 	PETREPORT_PET_TYPE_BIRD: PetReport.get_pet_breeds(PETREPORT_PET_TYPE_BIRD),
	  PETREPORT_PET_TYPE_RABBIT: PetReport.get_pet_breeds(PETREPORT_PET_TYPE_RABBIT),
	  PETREPORT_PET_TYPE_TURTLE: PetReport.get_pet_breeds(PETREPORT_PET_TYPE_TURTLE),
	  PETREPORT_PET_TYPE_SNAKE: PetReport.get_pet_breeds(PETREPORT_PET_TYPE_SNAKE),
	}

	#Majority of PetReports are cross-posted, so let's add contact information in.
	random_var = random.random()
	if random_var < 0.60:
		pr.contact_name = random.choice(USER_NAMES)
		pr.contact_email = generate_string(6) + '(at)' + 'test.com'
		pr.contact_number = generate_string(10, phone=True)
		pr.contact_link = generate_string(100, url=True)

	#Randomly generate attributes, or not.
	if status == "Found":
		if random.random() > 0.5:
			pr.pet_name = random.choice(PETREPORT_NAMES) 	
		if random.random() > 0.3:
			pr.description = generate_lipsum_paragraph(PETREPORT_DESCRIPTION_LENGTH) 
			pr.tag_info = generate_string(PETREPORT_TAG_INFO_LENGTH)
		if random.random() > 0.3:
			pr.breed = random.sample(breeds[pr.pet_type], 1)[0]
		if random.random() > 0.25:
			pr.geo_location_long = random.randrange(-180.0, 180.0)
			pr.geo_location_lat = random.randrange(-90.0, 90.0)

	#The Pet Owner knows his/her own pet.
	else:
		pr.pet_name = random.choice(PETREPORT_NAMES)
		pr.description = generate_lipsum_paragraph(PETREPORT_DESCRIPTION_LENGTH)
		pr.breed = random.sample(breeds[pr.pet_type], 1)[0]
		pr.tag_info = generate_string(PETREPORT_TAG_INFO_LENGTH)

	#Need to handle the cases where the contact might/might not have a photo for this PetReport!
	if random.random() <= 0.95:
		load_PetReport_sample_images()

		if pr.pet_type == PETREPORT_PET_TYPE_DOG:
			pr.img_path = pr.thumb_path = random.choice(PETREPORT_SAMPLE_DOG_IMAGES)
		elif pr.pet_type == PETREPORT_PET_TYPE_CAT:
			pr.img_path = pr.thumb_path = random.choice(PETREPORT_SAMPLE_CAT_IMAGES)
		elif pr.pet_type == PETREPORT_PET_TYPE_BIRD:
			pr.img_path = pr.thumb_path = random.choice(PETREPORT_SAMPLE_BIRD_IMAGES)
		elif pr.pet_type == PETREPORT_PET_TYPE_HORSE:
			pr.img_path = pr.thumb_path = random.choice(PETREPORT_SAMPLE_HORSE_IMAGES)			
		elif pr.pet_type == PETREPORT_PET_TYPE_RABBIT:
			pr.img_path = pr.thumb_path = random.choice(PETREPORT_SAMPLE_RABBIT_IMAGES)
		elif pr.pet_type == PETREPORT_PET_TYPE_SNAKE:
			pr.img_path = pr.thumb_path = random.choice(PETREPORT_SAMPLE_SNAKE_IMAGES)
		elif pr.pet_type == PETREPORT_PET_TYPE_TURTLE:
			pr.img_path = pr.thumb_path = random.choice(PETREPORT_SAMPLE_TURTLE_IMAGES)
		else:
			pr.img_path = pr.thumb_path = PETREPORT_UPLOADS_DEFAULT_OTHER_IMAGE

	else:
		#Set the img and thumb paths.
		pr.set_images (None, save=False)

	#Need to save (most of the time).
	if save == False:
		return pr
	else:
		pr.save()
		pr.workers = create_random_Userlist()
		Activity.log_activity("ACTIVITY_PETREPORT_SUBMITTED", user.userprofile, pr)
		return pr

#Find all potential PetMatch PetReport (Lost, Found) pairs and return a list of them.
def get_potential_PetMatch_PetReport_pairs(pet_type=None):

	if pet_type == None:
		allpets = PetReport.objects.all()
	else:
		allpets = PetReport.objects.all(pet_type=pet_type)

	#Organize and filter based on status
	lostpets = allpets.filter(status = "Lost")
	foundpets = allpets.filter(status = "Found")
	#This list will contain any potential matches that can be made.
	potential_matches = []

	#Iterate through both lists and find potential matches.
	for lostpet in lostpets:
		for foundpet in foundpets:
			if lostpet.pet_type == foundpet.pet_type:
				potential_matches.append((lostpet, foundpet))

	return potential_matches


#Create Random Object for: PetMatch
def create_random_PetMatch(lost_pet=None, found_pet=None, user=None, pet_type=None, threshold_bias=False, success_bias=False):
	#If the lost or found pet (or both) wasn't supplied, then search for potential PetMatch PetReport pairs
	if lost_pet == None or found_pet == None:

		#Get some potential matches
		potential_matches = get_potential_PetMatch_PetReport_pairs(pet_type=pet_type)
		if len(potential_matches) == 0:
			print_error_msg ("Can't create random PetMatch: There isn't at least one lost and found %s." % pet_type)
			return None
		
		#Get a random match.	
		potential_match = random.choice(potential_matches)

		if(lost_pet == None):
			lost_pet = potential_match[0]
		if(found_pet == None):
			found_pet = potential_match[1]

	#If no user supplied, then get a random one.
	if(user == None):
		user = random.choice(User.objects.all())

	#Make your PetMatch.
	pm = PetMatch(lost_pet = lost_pet, found_pet = found_pet, proposed_by = user.userprofile)
	(petmatch, outcome) = pm.save()

	#If the PetMatch save was successful...
	if (petmatch != None):
		if outcome == "NEW PETMATCH":
			#petmatch.is_open = random.choice ([True, False])
			user_count = len(UserProfile.objects.all())

			#if threshold_bias is True, the petmatch has a chance of reaching the threshold.
			if threshold_bias == True and random.randint(1,2) == 1:
				up_votes = create_random_Userlist(num_users=random.randint(5, VERIFICATION_DEFAULT_THRESHOLD))
				down_votes = create_random_Userlist(num_users=random.randint(5, VERIFICATION_DEFAULT_THRESHOLD))
				petmatch.down_votes = set(down_votes) - set(up_votes)
				petmatch.up_votes = set(up_votes)
				
			else:
				up_votes = create_random_Userlist(num_users=random.randint(0, VERIFICATION_DEFAULT_THRESHOLD/4))
				down_votes = create_random_Userlist(num_users=random.randint(0, VERIFICATION_DEFAULT_THRESHOLD/4))
				petmatch.down_votes = set(down_votes) - set(up_votes)
				petmatch.up_votes = set(up_votes) - set(down_votes)

			Activity.log_activity("ACTIVITY_PETMATCH_PROPOSED", user.userprofile, petmatch)
		
		elif outcome == "SQL UPDATE":
			petmatch.up_votes.add(user.userprofile)
			Activity.log_activity("ACTIVITY_PETMATCH_UPVOTE", user.userprofile, petmatch)			

	else:
		if outcome =="DUPLICATE PETMATCH":
			existing_petmatch = PetMatch.get_PetMatch(lost_pet, found_pet)

			if random.random() >= 0.5:
				existing_petmatch.up_votes.add(user.userprofile)
				existing_petmatch.down_votes.remove(user.userprofile)
				Activity.log_activity("ACTIVITY_PETMATCH_UPVOTE", user.userprofile, existing_petmatch)				
			else:
				existing_petmatch.down_votes.add(user.userprofile)
				existing_petmatch.up_votes.remove(user.userprofile)
				Activity.log_activity("ACTIVITY_PETMATCH_DOWNVOTE", user.userprofile, existing_petmatch)				
			
	print "\n"
	#Return the (possibly None) PetMatch
	return petmatch


''' Function for setting up User (with passwords and optionally following lists), Client, PetReport, and PetMatch objects for testing purposes.'''
def setup_objects(delete_all_objects=True, create_users=True, num_users=NUMBER_OF_TESTS, create_following_lists=False, create_bookmark_lists = False, create_clients=True, 
	num_clients=NUMBER_OF_TESTS, create_petreports=False, num_petreports=NUMBER_OF_TESTS, create_petmatches=False, num_petmatches=NUMBER_OF_TESTS, allow_closed_matches=False):

	#Setup the Site (if it hasn't yet been done)
	site = Site.objects.get_current()
	if (settings.DEBUG == True) and (site.domain != "localhost:8888"):
		site.domain ="localhost:8000"
		site.name = "localhost:8000"
		site.save()
		print_success_msg("Localhost Site successfully setup @ localhost:8888. Make sure Nginx has port 8888 configured in proxy.conf settings.")
	
	#Check if there's anything to do.
	if create_users == False and create_clients == False and create_petreports == False and create_petmatches == False:
		print_info_msg ("Nothing to do in setup_objects().")
		return False

	#Results Dictionary containing objects.
	results = {}	

	#Firstly, delete everything existing.
	if delete_all_objects == True:
		delete_all(leave_Users=False)
	else:
		delete_all(leave_Users=False)

	#Need to setup the object lists. The users list encapsulates tuples of <user, password>
	users = [(None, None) for i in range (num_users)]
	clients = [None for i in range (num_clients)]
	petreports = [None for i in range (num_petreports)]
	petmatches = [] #Cannot determine size of petmatch list up front.

	#First, create random Users
	if create_users == True:
		for i in range (num_users):
			(user, password) = create_random_User(i, pretty_name=True)
			users [i] = (user, password)
		results ["users"] = users	

		#Then, create the Users' following lists (if specified)
		if create_following_lists == True:
			for user in results ["users"]:
				userprofile = user[0].userprofile
				create_random_following_list(userprofile)

	#Then, create the Client objects (if specified)
	if create_clients == True:
		for i in range (num_clients):
			clients [i] = Client (enforce_csrf_checks=False)
		results ["clients"] = clients

	#Then, create random PetReport objects (if specified)
	if create_petreports == True:
		for i in range (num_petreports):
			(user, password) = random.choice(users)
			petreports [i] = create_random_PetReport(user=user)
		results ["petreports"] = petreports

		#Then, create the Users' bookmarks lists (if specified)
		if create_bookmark_lists == True:
			for user in results["users"]:
				userprofile = user[0].userprofile
				create_random_bookmark_list(userprofile)

	#Finally, create PetMatch objects (if specified)
	if create_petmatches == True:
		for i in range (num_petmatches):
			if allow_closed_matches == True:
				petmatch = create_random_PetMatch(threshold_bias=False, success_bias=True)
			else:
				petmatch = create_random_PetMatch(threshold_bias=False)

			#If we get back None, try again.
			if petmatch == None:
				continue

			petmatches.append(petmatch)
		results ["petmatches"] = petmatches

	#Return the full dictionary.
	return results

if __name__ == "__main__":
	#When Executed: Setup our fixture
	if (len(sys.argv) < 2) == True or (len(sys.argv) > 3) == True:
		print_error_msg ("You must specify one command argument:\n")
		print "\t 'setup' for setting up all model objects"
		print "\t 'onlyusers' for just creating users - no other model objects."
		print "\t 'wipeout' for wiping out all model objects\n"
		sys.exit()

	#Command Argument
	argument = sys.argv[1]

	if argument == "setup":
		results = setup_objects(create_users=True, create_bookmark_lists=True, create_following_lists=True, num_users=NUM_USERS, create_petreports=True, num_petreports=NUM_PETREPORTS, create_petmatches=True, num_petmatches=NUM_PETMATCHES)

		print_info_msg("%d PetMatches generated" % NUM_PETMATCHES)
		print_info_msg("%d PetReports generated" % NUM_PETREPORTS)
		print_info_msg("%d Users generated:" % NUM_USERS)

		for l in results["users"]:
			print l

	elif argument == "onlyusers":
		results = setup_objects(create_users=True, num_users=NUM_USERS)
		print_info_msg("%d Users generated:" % NUM_USERS)

		for l in results ["users"]:
			print l

	elif argument == "wipeout":
		delete_all(leave_Users=False)
		print_info_msg ("All model objects have been cleared from the database.")

	elif argument == "performance":
		print_info_msg("Going to Run Performance Benchmarks on EPM...")
		#Test Memory Usage
		#Test Response Time
		#Test CPU Usage
				




	else:
		print_error_msg("You must specify one command argument:\n")
		print "\t 'setup' for setting up all model objects"
		print "\t 'onlyusers' for just creating users - no other model objects."
		print "\t 'wipeout' for wiping out all model objects\n"
		sys.exit()
