from socializing.models import UserProfile
from utilities.utils import *
from utilities.constants import *
from django.contrib.auth import authenticate
import string, random, sys, os, random

'''===================================================================================
reputation_analysis.py: Script file for executing various analysis functions to
better understand user reputation.

NOTE: It's better if you run this file within the django shell. That way, you can manipulate
the variables within the console and run your experiment functions again.
==================================================================================='''

#Control Variables
NUM_ITERATIONS = 100 #Increase for greater approximation (more time required)
NUM_PETREPORTS = 100
NUM_USERS = 50
NUM_PETMATCHES = 50
EXPERIENCED_THRESHOLD = 500
EXPERT_THRESHOLD = 1000

#Given a UserProfile instance and a threshold, randomnly generate all available activities
#for this UserProfile and determine how many of them will reach the threshold.
def UserProfile_has_reached_threshold(userprofile, threshold):

	assert isinstance(userprofile, UserProfile)
	#Grab all of the activities into a list.
	activities = [ACTIVITY_PETREPORT_SUBMITTED, ACTIVITY_PETMATCH_PROPOSED, ACTIVITY_PETMATCH_UPVOTE, ACTIVITY_PETMATCH_DOWNVOTE]

	#Logistical Stuff
	username = userprofile.user.username
	mean_activities = 0.0 
	mean_activity_distribution = [0 for i in range(len(activities))]

	for i in range(NUM_ITERATIONS):

		#Start from a blank slate.
		userprofile.reputation = 0.0
		num_activities = 0		
		activity_distribution = [0 for i in range(len(activities))]

		while (userprofile.reputation < threshold):
			activity = random.choice (activities)

			#This is where Mazin's code goes:
			if activity == ACTIVITY_PETREPORT_SUBMITTED:
				userprofile.reputation += 5
				activity_distribution[0] += 1
			elif activity == ACTIVITY_PETMATCH_PROPOSED:
				userprofile.reputation += 5
				activity_distribution[1] += 1
			elif activity == ACTIVITY_PETMATCH_UPVOTE:
				userprofile.reputation += 2
				activity_distribution[2] += 1
			elif activity == ACTIVITY_PETMATCH_DOWNVOTE:
				userprofile.reputation += 2
				activity_distribution[3] += 1

			num_activities += 1

		mean_activities += num_activities

		#Collect all activity-specific values
		for i in range(len(activities)):
			mean_activity_distribution[i] += activity_distribution[i]

		print "[OK]: %s performed %d activities to reach threshold [%d]" % (username, num_activities, threshold)	
		print "[OK]: Distribution of activities: %s" % activity_distribution
		print "\n"

	#Now, collect the mean of all activity-specific values
	for i in range (len(activities)):
		v = mean_activity_distribution[i]
		mean_activity_distribution[i] = v/NUM_ITERATIONS

	print "[OK]: Iteration finished."
	print "[OK]: Mean of Activities completed before threshold reached: %d" % (mean_activities/NUM_ITERATIONS)
	print "[OK]: Mean of distribution of activities: %s" % mean_activity_distribution

	#Use matplotlib to plot this bar graph and show distribution.











