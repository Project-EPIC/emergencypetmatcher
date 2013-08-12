from home.models import *
from utils import *
from django.contrib.auth import authenticate
import string, random, sys, os
os.environ['DJANGO_SETTINGS_MODULE']='project.settings'

'''===================================================================================
setup_model_fixture.py: Setup sample (random) data for your dev env.
==================================================================================='''

#Control Variables
NUM_PETREPORTS = 300
NUM_USERS = 15
NUM_PETMATCHES = 100

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
	results = setup_objects(create_users=True, num_users=NUM_USERS, create_petreports=True, 
		num_petreports=NUM_PETREPORTS, create_petmatches=True, num_petmatches=NUM_PETMATCHES)

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

else:
	print_error_msg("You must specify one command argument:\n")
	print "\t 'setup' for setting up all model objects"
	print "\t 'onlyusers' for just creating users - no other model objects."
	print "\t 'wipeout' for wiping out all model objects\n"
	sys.exit()

	
