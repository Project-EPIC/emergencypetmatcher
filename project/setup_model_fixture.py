import string, random, sys, os
os.environ['DJANGO_SETTINGS_MODULE']='project.settings'
from home.models import *
from utils import *
from django.contrib.auth import authenticate


'''===================================================================================
setup_model_fixture.py: Setup sample (random) data for your dev env.
==================================================================================='''

#Control Variables
NUM_PETREPORTS = 100
NUM_USERS = 50
NUM_PETMATCHES = 50

#When Executed: Setup our fixture
if (len(sys.argv) < 2) == True or (len(sys.argv) > 3) == True:
	print "[ERROR]: You must specify at least one argument or at most 2 arguments (not including the python script name):\n"
	print "\t'setup' for setting up all data"
	print "\t\t 'onlyusers' for just creating users - no other model objects."
	print "\t'wipeout' for wiping out all data"
	print "\t\t 'leaveusers' for wiping out all data EXCEPT users"
	print ""
	sys.exit()

if sys.argv[1] == 'wipeout':

	if len(sys.argv) > 2 and sys.argv [2] == 'leaveusers':
		delete_all(leave_users=True)
		print '[OK]: All data from model objects EXCEPT User and UserProfile have been wiped out.'

	elif len(sys.argv) > 2:
		print "[ERROR]: Invalid use of 'wipeout'. Please try again."

	else:
		delete_all(only_test_users=True)
		print '[OK]: All data has been wiped out.'	

	sys.exit()

elif sys.argv[1] == 'setup':

	print '\n[INFO]: Setting up model fixture....'
	delete_all(only_test_users=True)
	users = []
	passwords = []

	if len(sys.argv) > 2 and sys.argv [2] == 'onlyusers':
		#Loop the old-fashioned way: We need to iterate again sometimes in order to get #NUM_USER of Users.
		index = 0
		while index != NUM_USERS:
			try:
				user, pwd = create_random_User(index)
				users.append(user)
				passwords.append(pwd)
				index += 1

			except Exception as e:
				print "[ERROR]: Problem when creating a random User (%s)" % e
				continue #Need to try (index) again.
			

		print '[OK]: %d Users created.' % (NUM_USERS)

	else:
		#Loop the old-fashioned way: We need to iterate again sometimes in order to get #NUM_USER of Users.
		index = 0
		while index != NUM_USERS:
			try:
				user, pwd = create_random_User(index)
				users.append(user)
				passwords.append(pwd)
				index += 1

			except Exception as e:
				print "[ERROR]: Problem when creating a random User (%s)" % e
				continue #Need to try (index) again.

		allusers = UserProfile.objects.all()
		print '[OK]: %d Users created.' % (len(User.objects.all()))
		num_lost = 0
		num_found = 0

		for i in range (NUM_PETREPORTS):
			pr = create_random_PetReport(random.choice(users))
			if pr.status == "Lost":
				num_lost += 1
			else:
				num_found += 1

		print '[OK]: %d Pet Reports created, %d LOST, %d FOUND' % (len(PetReport.objects.all()), num_lost, num_found)	

		for i in range (NUM_PETMATCHES):
			create_random_PetMatch(None,None,None)

		print '[OK]: (n <= %s) = %d Pet Matches created (Some PetMatch objects could not be created due to uniqueness constraints)' % (NUM_PETMATCHES, len(PetMatch.objects.all()))	
	print 'usernames with passwords are:'

	for i in range (NUM_USERS):
		print '<%s, %s>' % (users[i].username, passwords[i])

else:
	print '[ERROR]: Invalid argument(s). Try again.'







	