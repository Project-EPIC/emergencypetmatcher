import random, string, sys, time
from home.models import *

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
test_utils.py: Utility Functions for EPM Testing

When writing your test file (tests.py), make sure to have the following import:

	import test_utils as utils
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#Control Variable
NUMBER_OF_TESTS = 100
#Small List of Names
NAMES = ['Jacob', 'Emily', 'Joshua', 'Madison', 'Kenneth', 'Mark', 'Dave', 'Angela', '' 'Matthew', 'Olivia', 'Daniel', 'Hannah', 
'Chris', 'Abby', 'Andrew', 'Isabella', 'Mario', 'Sahar', 'Amrutha', 'Leysia', 'Ken', 'Abe']

#URLS
TEST_LOGIN_URL = '/login'
TEST_HOME_URL = '/'
TEST_SUBMIT_PETREPORT_URL ='/reporting/submit_petreport'
TEST_PETREPORT_URL ='/reporting/petreport/'
TEST_USERPROFILE_URL = '/users/'

#Generate a random alpha-numeric string.
def generate_string (size, chars = string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for i in range(size))

#Keep the user/tester updated.
def output_update (i):	
	output = "%d of %d iterations complete" % (i, NUMBER_OF_TESTS)
	sys.stdout.write("\r\x1b[K"+output.__str__())
	sys.stdout.flush()

#Give the lap time (and AVG) for a 'critical section'.
def performance_report(total_time):
	print '\tTotal Time: %s sec' % (total_time)
	print '\tAVG Time Taken for a Single Test: %s sec' % (total_time/NUMBER_OF_TESTS)

#Create Random Object for: User
def create_random_User(i, pretty_name=True):
	if pretty_name == True:
		username = random.choice(NAMES) + str(i)
	else:
		username = generate_string(10) + str(i)

	password = generate_string(10)
	email = generate_string(6) + '@' + 'test.com'
	user = User.objects.create_user(username = username, email = email, password = password)
	return (user, password)

#Create Random Object for: PetReport
def create_random_PetReport(user):
	pet_type = random.choice(PET_TYPE_CHOICES)[0]
	status = random.choice(STATUS_CHOICES)[0]
	pr = PetReport (pet_type = pet_type, status = status, proposed_by = user.get_profile())
	pr.pet_name = generate_string(30)
	pr.date_lost_or_found = "2012-07-18"
	pr.description = generate_string(300)
	pr.sex = random.choice(SEX_CHOICES)[0]
	pr.location = generate_string(50)
	pr.color = generate_string(20)
	pr.breed = generate_string(30)
	pr.size = random.choice(SIZE_CHOICES)[0]
	pr.age = random.randrange(0,15)
	pr.save()
	pr.workers = create_random_Userlist(-1,False,None)

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
	if leave_users == False:
		User.objects.all().delete()

#returns a random list of users or a list of friends for a user (when friends = True)
def create_random_Userlist(num_users = -1,friends=False,user=None):
	allusers = UserProfile.objects.all()
	if(num_users==-1):
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
def create_random_PetMatch(lostpet=None,foundpet=None,user=None):
	#to be modified to make unique petmatches
	allpets = PetReport.objects.all()
	prlost = allpets.filter(status = "Lost")
	prfound = allpets.filter(status = "Found")
	if(lostpet == None):
		lostpet = random.choice(prlost)
	if(foundpet == None):
		foundpet = random.choice(prfound)
	if(user == None):
		user = random.choice(User.objects.all())

	pm = PetMatch(lost_pet = lostpet, found_pet = foundpet, proposed_by = user.get_profile())
	pm.save()	
	pm.score = random.randrange(0, 10000)
	pm.is_open = random.choice ([True, False])
	user_count = UserProfile.objects.all().count()
	up_votes = create_random_Userlist(random.randint(1,((user_count/2)+1)),False,None)
	down_votes = UserProfile.objects.all()	
	
	for up_vote in up_votes:
			try:
				down_votes = down_votes.exclude(id  = up_vote.id)
			except ValueError:
				continue
	pm.up_votes = up_votes
	pm.down_votes = down_votes
	pm.save()
	return pm


			















