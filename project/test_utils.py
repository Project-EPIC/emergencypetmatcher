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
NAMES = ['Jacob', 'Emily', 'Joshua', 'Madison', 'Matthew', 'Olivia', 'Daniel', 'Hannah', 
'Chris', 'Abby', 'Andrew', 'Isabella', 'Mario', 'Sahar', 'Amrutha', 'Leysia', 'Ken', 'Abe']

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
	status = u'%s' % random.choice(STATUS_CHOICES)[0]
	pr = PetReport (pet_type = pet_type, status = status, proposed_by = user.get_profile())
	pr.pet_name = generate_string(30)
	pr.description = generate_string(300)
	pr.sex = random.choice(SEX_CHOICES)[0]
	pr.location = generate_string(50)
	pr.color = generate_string(20)
	pr.breed = generate_string(30)
	pr.size = random.choice(SIZE_CHOICES)[0]
	pr.age = random.randrange(0,15)
	pr.save()
	return pr

#Create Random Object for: PetMatch
def create_random_PetMatch(pr1, pr2, user):
	pm = PetMatch (lost_pet = pr1, found_pet = pr2, proposed_by = user.get_profile())
	pm.score = random.randrange(0, 10000)
	pm.is_open = random.choice ([True, False])
	pm.save()
	return pm

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











