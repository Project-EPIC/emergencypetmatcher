from home.models import *
from django.contrib.auth import authenticate
from django.test.client import Client
from django.forms.models import model_to_dict
import unittest, string, random, sys, time
import test_utils as utils

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
MatchingTesting: Testing for EPM Matching
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class MatchingTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		User.objects.all().delete()
		UserProfile.objects.all().delete()
		PetMatch.objects.all().delete()
		PetReport.objects.all().delete()
		Chat.objects.all().delete()
		ChatLine.objects.all().delete()

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		User.objects.all().delete()
		UserProfile.objects.all().delete()
		PetMatch.objects.all().delete()
		PetReport.objects.all().delete()
		Chat.objects.all().delete()
		ChatLine.objects.all().delete()

	def test_get_matching_interface(self):
		print '>>>> Testing test_get_matching_interface for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, passwords, clients, petreports) = utils.create_test_view_setup(create_petreports=True)

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			client_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			petreport_i = random.randrange(0, utils.NUMBER_OF_TESTS)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]
			petreport = petreports [petreport_i]

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print "\n%s logs onto %s to enter the matching interface..." % (user, client)

			#Go to the PRDP Page
			prdp_url = utils.TEST_PRDP_URL + str(petreport.id) + "/"
			response = client.get(prdp_url)
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], prdp_url)
			print "\n%s has successfully requested page %s..." % (user, prdp_url)  

			#From here, go to the matching interface
			matching_url = utils.TEST_MATCHING_URL + str(petreport.id) + "/"
			response = client.get(matching_url)

			#Generate the PetReport filters for this target PetReport so we take care of the case where there are NO PetReports to match! (causes a 302)
			filtered_pet_reports = PetReport.objects.all().exclude(pk=petreport.id).exclude(status = petreport.status).filter(pet_type = petreport.pet_type)
			if len(filtered_pet_reports) == 0:
				self.assertEquals(response.status_code, 302)
				print "Oh! There are no PetReports to match this PetReport with - Back to the Home Page!"

			else:
				self.assertEquals(response.status_code, 200)
				print "\n%s has successfully requested page %s..." % (user, matching_url)  	

			
			self.assertEquals(response.request ['PATH_INFO'], matching_url)	
			client.logout()	
			utils.output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		utils.performance_report(iteration_time)			

	def test_get_propose_match_dialog (self):
		print '>>>> Testing test_get_propose_match_dialog for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, passwords, clients, petreports) = utils.create_test_view_setup(create_petreports=True)

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			client_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			petreport_i = random.randrange(0, utils.NUMBER_OF_TESTS)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]
			petreport = petreports [petreport_i]

			print "\n%s logs onto %s to enter the matching interface..." % (user, client)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)

			#Go to the matching interface
			matching_url = utils.TEST_MATCHING_URL + str(petreport.id) + "/"
			print matching_url
			response = client.get(matching_url)

			#Generate the PetReport filters for this target PetReport so we take care of the case where there are NO PetReports to match! (causes a 302)
			filtered_pet_reports = PetReport.objects.all().exclude(pk=petreport.id).exclude(status = petreport.status).filter(pet_type = petreport.pet_type)
			if len(filtered_pet_reports) == 0:
				self.assertEquals(response.status_code, 302)
				print "Oh! There are no PetReports to match this PetReport with - Back to the Home Page!"
				continue

			self.assertEquals(response.status_code, 200)
			print "\n%s has successfully requested page %s..." % (user, matching_url)  				

			#PetReport filters
			filtered_pet_reports = PetReport.objects.all().exclude(pk=petreport.id).exclude(status = petreport.status).filter(pet_type = petreport.pet_type)
			candidate_petreport = random.choice(filtered_pet_reports)

			#Go to the propose match dialog
			propose_match_url = utils.TEST_PROPOSE_MATCH_URL + str(petreport.id) + "/" + str(candidate_petreport.id) + "/"
			response = client.get(propose_match_url)
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], propose_match_url)			

			utils.output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		utils.performance_report(iteration_time)	


	def test_post_good_propose_match (self):
		print '>>>> Testing test_post_propose_match for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, passwords, clients, petreports) = utils.create_test_view_setup(create_petreports=True)
		num_petmatches = 0

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			client_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			petreport_i = random.randrange(0, utils.NUMBER_OF_TESTS)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]
			petreport = petreports [petreport_i]

			print "\n%s logs onto %s to enter the matching interface..." % (user, client)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)

			#Go to the matching interface
			matching_url = utils.TEST_MATCHING_URL + str(petreport.id) + "/"
			response = client.get(matching_url)

			#Generate the PetReport filters for this target PetReport so we take care of the case where there are NO PetReports to match! (causes a 302)
			filtered_pet_reports = PetReport.objects.all().exclude(pk=petreport.id).exclude(status = petreport.status).filter(pet_type = petreport.pet_type)
			if len(filtered_pet_reports) == 0:
				self.assertEquals(response.status_code, 302)
				print "Oh! There are no PetReports to match this PetReport with - Back to the Home Page!"
				continue

			self.assertEquals(response.status_code, 200)
			print "\n%s has successfully requested page '%s'..." % (user, matching_url) 
			candidate_petreport = random.choice(filtered_pet_reports) 

			#Go to the propose match dialog
			propose_match_url = utils.TEST_PROPOSE_MATCH_URL + str(petreport.id) + "/" + str(candidate_petreport.id) + "/"
			response = client.get(propose_match_url)
			print "\n%s has successfully requested page '%s'..." % (user, propose_match_url) 

			#Make the POST request Call		
			description = utils.generate_lipsum_paragraph()
			post = {'description': description}
			response = client.post(propose_match_url, post, follow=True)
			client.logout()						

			#Grab the PetMatch that has either been posted in the past or has been posted by this User.
			match = PetMatch.get_PetMatch(petreport, candidate_petreport)
			if match.user_has_voted(user.get_profile()) == True:
				print "A PetMatch already exists with these two PetReports, and so %s has up-voted this match!" % (user)
			else:
				print "%s has successfully POSTED a new match!" % (user)				
				num_petmatches += 1

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(len(response.redirect_chain), 1)
			self.assertEquals(response.redirect_chain[0][0], 'http://testserver/')
			self.assertEquals(response.redirect_chain[0][1], 302)
			self.assertEquals(response.request ['PATH_INFO'], utils.TEST_HOME_URL)				

			#Some checks for the PetMatch objects stored
			self.assertTrue(len(PetMatch.objects.all()) == num_petmatches or len(PetMatch.objects.all()) <= i)
			utils.output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		utils.performance_report(iteration_time)


	def test_post_bad_propose_match (self):
		print '>>>> Testing test_post_propose_match for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, passwords, clients, petreports) = utils.create_test_view_setup(create_petreports=True)
		num_petmatches = 0

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			client_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			petreport_i = random.randrange(0, utils.NUMBER_OF_TESTS)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]
			petreport = petreports [petreport_i]

			print "\n%s logs onto %s to enter the matching interface..." % (user, client)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)

			#Go to the matching interface
			matching_url = utils.TEST_MATCHING_URL + str(petreport.id) + "/"
			response = client.get(matching_url)

			#Generate the PetReport filters for this target PetReport so we take care of the case where there are NO PetReports to match! (causes a 302)
			filtered_pet_reports = PetReport.objects.all().exclude(pk=petreport.id).exclude(status = petreport.status).filter(pet_type = petreport.pet_type)
			if len(filtered_pet_reports) == 0:
				self.assertEquals(response.status_code, 302)
				print "Oh! There are no PetReports to match this PetReport with - Back to the Home Page!"
				continue

			self.assertEquals(response.status_code, 200)
			print "\n%s has successfully requested page '%s'..." % (user, matching_url) 
			candidate_petreport = random.choice(filtered_pet_reports) 

			#Go to the propose match dialog
			propose_match_url = utils.TEST_PROPOSE_MATCH_URL + str(petreport.id) + "/" + str(candidate_petreport.id) + "/"
			response = client.get(propose_match_url)
			print "\n%s has successfully requested page '%s'..." % (user, propose_match_url) 

			#The description is empty, so this POST should fail.
			description = "       "
			post = {'description': description}
			response = client.post(propose_match_url, post, follow=True)
			client.logout()					

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], propose_match_url)
			print "\n%s was NOT able to POST a successful match. That was to be expected!" % (user)

			#Some checks for the PetMatch objects stored
			self.assertTrue(len(PetMatch.objects.all()) == 0)
			utils.output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		utils.performance_report(iteration_time)	
















