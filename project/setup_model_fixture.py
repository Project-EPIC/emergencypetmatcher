import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'

from home.models import *
from django.contrib.auth import authenticate
import utils
import string, random, sys, os

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
setup_model_fixture.py: Setup sample (random) data for your dev env.
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

#Control Variables
NUM_PETREPORTS = 100
NUM_USERS = 50
NUM_PETMATCHES = 150

'''''''''''''''''''''''''''''''''''''''''''''''''''
When Executed: Setup our fixture
'''''''''''''''''''''''''''''''''''''''''''''''''''

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
		utils.delete_all(leave_users=True)
		print '[OK]: All data from model objects EXCEPT User and UserProfile have been wiped out.'
	elif len(sys.argv) > 2:
		print "[ERROR]: Invalid use of 'wipeout'. Please try again."
	else:
		utils.delete_all()
		print '[OK]: All data has been wiped out.'	
	sys.exit()

elif sys.argv[1] == 'setup':

	print '\nSetting up model fixture....'
	utils.delete_all()
	users = []
	passwords = []

	if len(sys.argv) > 2 and sys.argv [2] == 'onlyusers':
		for i in range (NUM_USERS):
			user, pwd = utils.create_random_User(i)
			users.append(user)
			passwords.append(pwd)
		allusers = UserProfile.objects.all()
		for user in allusers:
			user.friends = utils.create_random_Userlist(-1,True,user)#not working without supplying -1
		print '[OK]: %d Users created.' % (len(User.objects.all()))

	else:
		for i in range (NUM_USERS):
			user, pwd = utils.create_random_User(i)
			users.append(user)
			passwords.append(pwd)
		allusers = UserProfile.objects.all()
		print '[OK]: %d Users created.' % (len(User.objects.all()))

		for user in allusers:
			user.friends = utils.create_random_Userlist(-1,True,user)#not working without supplying -1

		num_lost = 0
		num_found = 0
		for i in range (NUM_PETREPORTS):
			pr = utils.create_random_PetReport(random.choice(users))
			if pr.status == "Lost":
				num_lost += 1
			else:
				num_found += 1


		print '[OK]: %d Pet Reports created, %d LOST, %d FOUND' % (len(PetReport.objects.all()), num_lost, num_found)	

		for i in range (NUM_PETMATCHES):
			utils.create_random_PetMatch(None,None,None)

		print '[OK]: (n <= %s) = %d Pet Matches created (Some PetMatch objects could not be created due to uniqueness constraints)' % (NUM_PETMATCHES, len(PetMatch.objects.all()))	
	print 'usernames with passwords are:'

	for i in range (NUM_USERS):
		print '<%s, %s>' % (users[i].username, passwords[i])

else:
	print '[ERROR]: Invalid argument(s). Try again.'







	