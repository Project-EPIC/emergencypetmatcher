from django.core.files.images import ImageFile
from django.forms.models import model_to_dict
from django.test.client import Client
from home.models import *
from constants import *
import random, string, sys, time, datetime, lipsum, traceback

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
epm_utils.py: Utility Functions for EPM Utility and Testing

When writing your test file (tests.py), make sure to have the following import:

	import epm_utils as utils
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#Control Variable
NUMBER_OF_TESTS = 50

#Setup Lorem Ipsum Generator
LIPSUM = lipsum.Generator()
LIPSUM.sentence_mean = 4
LIPSUM.sentence_sigma = 1
LIPSUM.paragraph_mean = 3
LIPSUM.paragraph_sigma = 1

#Generate a random alpha-numeric string.
def generate_string (size, chars = string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for i in range(size))

def generate_lipsum_paragraph(max_length):
	result =  LIPSUM.generate_paragraph()
	#Make sure that the length does not exceed max_length...
	if len(result) > max_length:
		return generate_lipsum_paragraph(max_length)
	else:
		return result

#Keep the user/tester updated.
def output_update (i):	
	output = "%d of %d iterations complete" % (i, NUMBER_OF_TESTS)
	sys.stdout.write("\r\x1b[K"+output.__str__())
	sys.stdout.flush()

#Helper function for cleaning up the modeldict passed in for simple displaying
def simplify_model_dict(model_object):
	assert isinstance (model_object, models.Model)
	modeldict = model_to_dict(model_object)

	#iterate through all fields in the model_dict
	for field in modeldict:
		value = modeldict[field]
		if isinstance(value, datetime.datetime) or isinstance(value, datetime.date):
			modeldict[field] = value.isoformat()
		elif isinstance(value, ImageFile):
			modeldict[field] = value.name
		elif field == "sex":
			modeldict[field] = model_object.get_sex_display()
		elif field == "size":
			modeldict[field] = model_object.get_size_display()

	#Just add a couple of nice attributes.
	modeldict ["proposed_by_username"] = model_object.proposed_by.user.username		
	return modeldict


''' 
generate_random_date():

Referenced from: http://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates

Get a time at a proportion of a range of two formatted times.
start and end should be strings specifying times formated in the
given format (strftime-style), giving an interval [start, end].
prop specifies how a proportion of the interval to be taken after
start.  The returned time will be in the specified format.
'''
def generate_random_date(start, end, format, prop):

    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))

#Give the lap time (and AVG) for a 'critical section'.
def performance_report(total_time):
	print '\tTotal Time: %s sec' % (total_time)
	print '\tAVG Time Taken for a Single Test: %s sec' % (total_time/NUMBER_OF_TESTS)

#Create Random Object for: User
def create_random_User(i, pretty_name=True):
	if pretty_name == True:
		username = random.choice(USERNAMES) + str(i)
	else:
		username = generate_string(10) + str(i)

	password = generate_string(10)
	email = generate_string(6) + '@' + 'test.com'
	user = User.objects.create_user(username = username, email = email, password = password)
	return (user, password)

#Create Random Object for: PetReport
def create_random_PetReport(user=None, status=None, pet_type=None):
	
	if pet_type == None:
		pet_type = random.choice(PET_TYPE_CHOICES)[0]
	if status == None:
		status = random.choice(STATUS_CHOICES)[0]
	if user == None:
		user = random.choice(User.objects.all())

	pr = PetReport (pet_type = pet_type, status = status, proposed_by = user.get_profile())

	pr.date_lost_or_found = generate_random_date(DATE_LOWER_BOUND, DATE_UPPER_BOUND, "%Y-%m-%d", random.random())
	pr.sex = random.choice(SEX_CHOICES)[0]
	pr.size = random.choice(SIZE_CHOICES)[0] 
	pr.location = generate_string(20) 
	pr.color = generate_string(20)

	#Randomly generate attributes, or not.
	if status == "Found":

		if random.random() > 0.5:
			pr.pet_name = random.choice(PETREPORT_NAMES) 	

		if random.random() > 0.3:
			pr.description = generate_lipsum_paragraph(500) 

		if random.random() > 0.3:
			pr.breed = generate_string(15) 

		if random.random() > 0.3:
			pr.age = str(random.randrange(0, 15))

	#The Pet Owner knows his/her own pet.
	else:
		pr.pet_name = random.choice(PETREPORT_NAMES)
		pr.description = generate_lipsum_paragraph(500)
		pr.breed = generate_string(15)
		pr.age = str(random.randrange(0, 15))

	pr.save()
	pr.workers = create_random_Userlist(-1, False, None)

	#Need to handle Image defaults...
	if pr.pet_type == "Dog":
		pr.img_path.name = "images/defaults/dog_silhouette.jpg"
	elif pr.pet_type == "Cat":
		pr.img_path.name = "images/defaults/cat_silhouette.jpg"
	elif pr.pet_type == "Horse":
		pr.img_path.name = "images/defaults/horse_silhouette.jpg"
	elif pr.pet_type == "Rabbit":
		pr.img_path.name = "images/defaults/rabbit_silhouette.jpg"
	elif pr.pet_type == "Snake":
		pr.img_path.name = "images/defaults/snake_silhouette.jpg"
	elif pr.pet_type == "Turtle":
		pr.img_path.name = "images/defaults/turtle_silhouette.jpg"
	else:
		pr.img_path.name = "images/defaults/other_silhouette.jpg"

	pr.save()
	return pr

#Create Random Object for: Chat
def create_random_Chat (pr):
	chat = Chat (pet_report = pr)
	chat.save()
	return chat

#Create Random Object for: ChatLine
def create_random_ChatLine(user, chat):
	chatline = ChatLine(userprofile = user.get_profile(), chat = chat)
	chatline.text = generate_string(100)
	chatline.save()
	return chatline

#Delete all model data
def delete_all(leave_users = False):
	PetMatch.objects.all().delete()
	PetReport.objects.all().delete()
	Chat.objects.all().delete()
	ChatLine.objects.all().delete()
	#Delete Users if you want to.
	if leave_users == False:
		User.objects.all().delete()

#returns a random list of users or a list of friends for a user (when friends = True)
def create_random_Userlist(num_users = -1, friends=False, user=None):
	allusers = UserProfile.objects.all()
	if(num_users == -1):
		num_users = random.randint(1,allusers.count())

	userlist = random.sample(allusers,num_users)

	if (friends == True):
		if(user != None):
			try:
				userlist.remove(user)
			except ValueError:
				return userlist

		elif (user == None):
			print "Insufficient arguments, list of friends was not created successfully."
			return userlist

	return userlist


#Create Random Object for: PetMatch
def create_random_PetMatch(lost_pet=None, found_pet=None, user=None, pet_type=None):
	
	#If the lost or found pet (or both) wasn't supplied, then get random Pet Reports.
	if lost_pet == None or found_pet == None:

		if pet_type == None:
			pet_type = random.choice(PET_TYPE_CHOICES)[0]

		allpets = PetReport.objects.filter(pet_type=pet_type)
		prlost = allpets.filter(status = "Lost")
		prfound = allpets.filter(status = "Found")

		if len(prlost.all()) == 0 or len(prfound.all()) == 0:
			print "[ERROR]: Can't create random PetMatch: There isn't at least one lost and found %s." % pet_type
			return None

		if(lost_pet == None):
			lost_pet = random.choice(prlost)
		if(found_pet == None):
			found_pet = random.choice(prfound)

	#If no user supplied, then get a random one.
	if(user == None):
		user = random.choice(User.objects.all())

	#Make your PetMatch.
	pm = PetMatch(lost_pet = lost_pet, found_pet = found_pet, proposed_by = user.get_profile(), description = generate_lipsum_paragraph(500))
	(petmatch, outcome) = pm.save()

	#If the PetMatch save was successful...
	if (petmatch != None):
		if outcome == "NEW PETMATCH":
			petmatch.score = random.randrange(0, 10000)
			petmatch.is_open = random.choice ([True, False])
			user_count = UserProfile.objects.all().count()
			up_votes = create_random_Userlist(random.randint(1,((user_count/2)+1)),False,None)
			down_votes = UserProfile.objects.all()	
			
			for up_vote in up_votes:
				try:
					down_votes = down_votes.exclude(id =up_vote.id)
				except ValueError:
					continue

			petmatch.up_votes = up_votes
			petmatch.down_votes = down_votes
			petmatch.save()
			log_activity(ACTIVITY_PETMATCH_PROPOSED, user.get_profile(), petmatch=petmatch)
		
		elif outcome == "SQL UPDATE":
			petmatch.up_votes.add(user.get_profile())
			log_activity(ACTIVITY_PETMATCH_UPVOTE, user.get_profile(), petmatch=petmatch)			

	else:
		if outcome =="DUPLICATE PETMATCH":
			existing_petmatch = PetMatch.get_PetMatch(lost_pet, found_pet)

			if random.random() >= 0.5:
				existing_petmatch.up_votes.add(user.get_profile())
				existing_petmatch.down_votes.remove(user.get_profile())
				log_activity(ACTIVITY_PETMATCH_UPVOTE, user.get_profile(), petmatch=existing_petmatch)				
			else:
				existing_petmatch.down_votes.add(user.get_profile())
				existing_petmatch.up_votes.remove(user.get_profile())
				log_activity(ACTIVITY_PETMATCH_DOWNVOTE, user.get_profile(), petmatch=existing_petmatch)				
			
	#Return the (possibly None) PetMatch
	return petmatch


''' Function for setting up Client, User (with passwords), and (optionally) PetReport objects for testing purposes.'''
def create_test_view_setup(create_petreports=False, create_petmatches=False):

	#Firstly, delete everything existing.
	delete_all()
	
	#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
	clients = [ None for i in range (NUMBER_OF_TESTS) ]
	users = [ None for i in range (NUMBER_OF_TESTS) ]
	passwords = [ None for i in range (NUMBER_OF_TESTS) ]
	petreports = [ None for i in range (NUMBER_OF_TESTS) ]
	petmatches = [ None for i in range (NUMBER_OF_TESTS/2) ]
	pet_type = random.choice(PET_TYPE_CHOICES)[0]
	status = None

	#Iterate w.r.t NUMBER_OF_TESTS control variable.
	for i in range (NUMBER_OF_TESTS):
		user, password = create_random_User(i, pretty_name=True)
		users [i] = user
		passwords [i] = password
		client = Client (enforce_csrf_checks=False)
		clients [i] = client

		if create_petreports == True:

			#reset the pet_type: This is done so that the pet reports are generated with one pet type per two Pet Reports.
			if i % 2 == 0:
				status = "Lost"
				pet_type = random.choice(PET_TYPE_CHOICES)[0]				
			else:
				status = "Found"

			pr = create_random_PetReport(user, status=status, pet_type=pet_type)
			petreports [i] = pr

		#We can only create AT MOST NUMBER_OF_TESTS/2 PetMatch objects in total, so we need to be careful about indices.
		#(i >= 1 and i <= NUMBER_OF_TESTS/2)
		if (create_petmatches == True) and (i % 2 == 1) and (i <= NUMBER_OF_TESTS/2):
			pm = create_random_PetMatch(lost_pet=petreports[i-1], found_pet=petreports[i], pet_type=pet_type, user=user)
			petmatches [i-1] = pm


	if create_petreports == True and create_petmatches == True:
		return (users, passwords, clients, petreports, petmatches)

	if create_petreports == True:
		return (users, passwords, clients, petreports)

	if create_petmatches == True:
		return (users, passwords, clients, petmatches)

	#just return the simple ones, geez!		
	return (users, passwords, clients)

			















