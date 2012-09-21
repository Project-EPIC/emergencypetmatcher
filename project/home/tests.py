from django.contrib.auth import authenticate
from django.test.client import Client
from utils import *
from home.models import *
from home import logging
import unittest, string, random, sys, time

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
ModelTesting: Testing for EPM Models
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class ModelTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all()
	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all()

	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: UserProfile + User
	'''''''''''''''''''''''''''''''''''''''''''''''''''
 	def test_save_User(self):
 		print_testing_name("test_save_User")
 		iteration_time = 0.00

 		for i in range (NUMBER_OF_TESTS):
 			start_time = time.clock()

			#Create the essential ingredients for the User object.
			#Creating a User creates a User Profile!
			user, password = create_random_User(i)
			username = user.username

			user_profile = user.get_profile()
			user_profile.reputation = random.randrange(0,100)
			user_profile.save()

			# check we can find the user in the database again
			user_prof = UserProfile.objects.get(user = user)
			self.assertEquals(user_profile, user_prof)
			user = user_prof.user

			#Now, use the authenticate function
			self.assertTrue(user.check_password(password) == True)
			userObject = authenticate (username = username, password = password)
			self.assertTrue(userObject is not None)

			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue (len(UserProfile.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == NUMBER_OF_TESTS)
		performance_report(iteration_time)


	def test_update_User (self):
		print_testing_name("test_update_User")
		iteration_time = 0.00

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User object.
			user, password = create_random_User(i)
			username = user.username

			user_profile = user.get_profile()
			user_profile.reputation = random.randrange(0,100)
			user_profile.save()

			# check that we can update the user's username
			changed_username = generate_string (10) + str(i)
			user.username = changed_username
			user.save()

			user_profile = UserProfile.objects.get(user = user)
			user = user_profile.user
			self.assertEqual (user.username, changed_username)
			self.assertNotEqual (user.username, username)

			#Now, use the authenticate function
			self.assertTrue(user.check_password(password) == True)
			userObject = authenticate (username = changed_username, password = password)
			self.assertTrue(userObject is not None)

			output_update (i + 1)		
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue (len(UserProfile.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == NUMBER_OF_TESTS)
		performance_report(iteration_time)

	def test_delete_User(self):
		print_testing_name("test_delete_User")
		iteration_time = 0.00

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User object.
			user, password = create_random_User(i)
			username = user.username

			user_profile = user.get_profile()
			user_profile.reputation = random.randrange(0,100)
			user_profile.save()

			User.objects.get(username = username).delete()
			self.assertTrue(len(UserProfile.objects.all()) == 0)
			self.assertTrue(len(User.objects.all()) == 0)

			#Now, use the authenticate function
			userObject = authenticate (username = username, password = password)
			self.assertTrue(userObject is None)
			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue(len(UserProfile.objects.all()) == 0)
		self.assertTrue(len(User.objects.all()) == 0)
		performance_report(iteration_time)

	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: PetReport
	'''''''''''''''''''''''''''''''''''''''''''''''''''
	def test_save_PetReport(self):
		print_testing_name("test_save_PetReport")
		iteration_time = 0.00

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User object.
			user, password = create_random_User(i)

			#Create the essential ingredients for the PetReport object.
			pr = create_random_PetReport(user)
			
			# check we can find the PetReport in the database again
			pet_report = PetReport.objects.get(proposed_by = user)
			self.assertEquals(pr.proposed_by, pet_report.proposed_by)
			self.assertEquals(pr.pet_type, pet_report.pet_type)
			self.assertEquals(pr.status, pet_report.status)
			self.assertEquals(pr.description, pet_report.description)
			self.assertEquals(pr.sex, pet_report.sex)
			self.assertEquals(pr.location, pet_report.location)
			self.assertEquals(pr.color, pet_report.color)
			self.assertEquals(pr.breed, pet_report.breed)
			self.assertEquals(pr.size, pet_report.size)
			self.assertEquals(pr.age, pet_report.age)
			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue (len(PetReport.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(UserProfile.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == NUMBER_OF_TESTS)
		performance_report(iteration_time)

	def test_updatePetReport(self):
		print_testing_name("test_updatePetReport")
		iteration_time = 0.00

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User object.
			user, password = create_random_User(i)

			#Create the essential ingredients for the PetReport object.
			pr = create_random_PetReport(user)

			#UPDATES
			pr.pet_name = generate_string (30)
			pr.description = generate_lipsum_paragraph(500)
			pr.sex = random.choice(SEX_CHOICES)[0]
			pr.location = generate_string (50)
			pr.color = generate_string (20)
			pr.breed = generate_string (30)
			pr.size = generate_string (30)
			pr.age = str(random.randrange(0,15))

			# check we can find the PetReport in the database again
			pr.save()
			pet_report = PetReport.objects.get(proposed_by = user)

			self.assertEquals(pr.proposed_by, pet_report.proposed_by)
			self.assertEquals(pr.pet_type, pet_report.pet_type)
			self.assertEquals(pr.status, pet_report.status)
			self.assertEquals(pr.description, pet_report.description)
			self.assertEquals(pr.sex, pet_report.sex)
			self.assertEquals(pr.location, pet_report.location)
			self.assertEquals(pr.color, pet_report.color)
			self.assertEquals(pr.breed, pet_report.breed)
			self.assertEquals(pr.size, pet_report.size)
			self.assertEquals(pr.age, pet_report.age)
			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue (len(PetReport.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(UserProfile.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == NUMBER_OF_TESTS)
		performance_report(iteration_time)

	def test_delete_PetReport(self):
		print_testing_name("test_delete_PetReport")
		iteration_time = 0.00

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User object.
			user, password = create_random_User(i)

			#Create the essential ingredients for the PetReport object.
			pr = create_random_PetReport(user)

			PetReport.objects.get(proposed_by = user).delete()
			self.assertTrue(len(PetReport.objects.all()) == 0)
			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue (len(UserProfile.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(User.objects.all()) == NUMBER_OF_TESTS)
		self.assertTrue (len(PetReport.objects.all()) == 0)
		performance_report(iteration_time)


	'''''''''''''''''''''''''''''''''''''''''''''''''''
	CRUD Tests for: PetMatch 
	'''''''''''''''''''''''''''''''''''''''''''''''''''
	def test_save_PetMatch(self):
		print_testing_name("test_save_PetMatch")
		iteration_time = 0.00

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User objects.
			user, password = create_random_User(str(i) + 'a')
			user2, password2 = create_random_User(str(i) + 'b')
			user3, password3 = create_random_User(str(i) + 'c')

			#Create the essential ingredients for the PetReport objects.
			pet_type = random.choice(PET_TYPE_CHOICES)[0]
			pr1 = create_random_PetReport(user2, status = "Lost", pet_type = pet_type)
			pr2 = create_random_PetReport(user3, status = "Found", pet_type = pet_type)

			#Now, create the PetMatch
			pm = create_random_PetMatch(pr1, pr2, user, pet_type=pet_type)

			#Now, retrieve it and assert that they are the same.
			pm_same = PetMatch.objects.get(proposed_by = user.get_profile())
			self.assertEqual(pm.lost_pet, pm_same.lost_pet)
			self.assertEqual(pm.found_pet, pm_same.found_pet)
			self.assertEqual(pm.proposed_by, pm_same.proposed_by)
			self.assertEqual(pm, pm_same)
			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(UserProfile.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == NUMBER_OF_TESTS)
		performance_report(iteration_time)


	def test_save_improperly_saved_PetMatch(self):
		print_testing_name("test_save_improperly_saved_PetMatch")
		iteration_time = 0.00

		start_time = time.clock()
		for i in range (NUMBER_OF_TESTS):

			create_random_User(str(i) + 'a')
			create_random_User(str(i) + 'b')
			pet_type = random.choice(PET_TYPE_CHOICES)[0]
			pr_lost = create_random_PetReport(status="Lost")
			pr_found = create_random_PetReport(status="Found")

			#Now, create an improperly-placed PetMatch (i.e. Lost on Found attribute, Found on Lost attribute).
			pm = create_random_PetMatch(lost_pet=pr_found, found_pet=pr_lost)

			self.assertEquals(pm, None)
			self.assertEquals(PetMatch.objects.filter(lost_pet=pr_found, found_pet=pr_lost).exists(), False)

			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(UserProfile.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == 0)
		performance_report(iteration_time)

	def test_save_duplicate_PetMatch(self):
		print_testing_name("test_save_duplicate_PetMatch")
		iteration_time = 0.00

		start_time = time.clock()
		for i in range (NUMBER_OF_TESTS):

			u1 = create_random_User(str(i) + 'a')
			u2 = create_random_User(str(i) + 'b')
			pet_type = random.choice(PET_TYPE_CHOICES)[0]
			pr_lost = create_random_PetReport(status="Lost")
			pr_found = create_random_PetReport(status="Found")
			pm = create_random_PetMatch(lost_pet=pr_lost, found_pet=pr_found, user = u1[0])
			pm_duplicate = create_random_PetMatch(lost_pet=pr_lost, found_pet=pr_found, user = u2[0])

			self.assertFalse(pm == None)
			self.assertEquals(pm_duplicate, None)
			self.assertEquals(PetMatch.objects.filter(lost_pet=pr_lost, found_pet=pr_found, proposed_by = u1[0]).exists(), True)			
			self.assertEquals(PetMatch.objects.filter(lost_pet=pr_lost, found_pet=pr_found, proposed_by = u2[0]).exists(), False)

			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(UserProfile.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == NUMBER_OF_TESTS)
		performance_report(iteration_time)		


	def test_update_PetMatch(self):
		print_testing_name("test_update_PetMatch")
		iteration_time = 0.00

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User objects.
			user, password = create_random_User(str(i) + 'a')
			user2, password2 = create_random_User(str(i) + 'b')
			user3, password3 = create_random_User(str(i) + 'c')

			#Create the essential ingredients for the PetReport objects.
			pet_type = random.choice(PET_TYPE_CHOICES)[0]
			pr1 = create_random_PetReport(user2, status = "Lost", pet_type = pet_type)
			pr2 = create_random_PetReport(user3, status = "Found", pet_type = pet_type)

			#Now, create the PetMatch
			pm = create_random_PetMatch(pr1, pr2, user, pet_type=pet_type)

			#UPDATES
			pm.score = random.randrange(0, 10000)
			pm.is_open = random.choice ([True, False])

			#Save it to the database.
			pm.save()
			pm_updated = PetMatch.objects.get(proposed_by = user.get_profile(), lost_pet = pr1, found_pet = pr2)

			#Now assert that the updated PetMatch matches the one we've just updated.
			self.assertEqual(pm, pm_updated)
			self.assertEqual(pm.score, pm_updated.score)
			self.assertEqual(pm.is_open, pm_updated.is_open)
			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(UserProfile.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == NUMBER_OF_TESTS)
		performance_report(iteration_time)


	def test_delete_PetMatch(self):
		print_testing_name("test_delete_PetMatch")
		iteration_time = 0.00

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#Create the essential ingredients for the User objects.
			user, password = create_random_User(str(i) + 'a')
			user2, password2 = create_random_User(str(i) + 'b')
			user3, password3 = create_random_User(str(i) + 'c')

			#Create the essential ingredients for the PetReport objects.
			pet_type = random.choice(PET_TYPE_CHOICES)[0]
			pr1 = create_random_PetReport(user2, status = "Lost", pet_type = pet_type)
			pr2 = create_random_PetReport(user3, status = "Found", pet_type = pet_type)

			#Now, create the PetMatch
			pm = create_random_PetMatch(pr1, pr2, user, pet_type=pet_type)

			#And now delete the PetMatch Object.
			PetMatch.objects.all().get(proposed_by = user.get_profile(), lost_pet = pr1, found_pet = pr2).delete()
			#Assert that there is nothing in the database!
			self.assertTrue(len(PetMatch.objects.all()) == 0)
			output_update (i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)			

		print ''
		self.assertTrue(len(User.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(UserProfile.objects.all()) == NUMBER_OF_TESTS * 3)
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS * 2)
		self.assertTrue(len(PetMatch.objects.all()) == 0)
		performance_report(iteration_time)



'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
LoginTesting: Testing for EPM Logging In/Out
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class LoginTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all()

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all()

	def test_login_Users_successfully(self):
		print_testing_name("test_login_Users_successfully")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, passwords, clients) = create_test_view_setup(create_petreports=False)	

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			user_i = random.randrange(0, NUMBER_OF_TESTS)
			client_i = random.randrange(0, NUMBER_OF_TESTS)
			user = users [user_i]
			client = clients [client_i]

			print "[INFO]:%s logs onto %s and attempts to login..." % (user, client)

			#Go to the Login Page
			response = client.get(URL_LOGIN)
			next = response.context ['next']
			self.assertTrue(response.status_code == 200)
			self.assertTrue(response.request ['PATH_INFO'] == URL_LOGIN)
			self.assertTrue(next == URL_HOME)

			#Submit Login information
			response = client.post (URL_LOGIN, 
				{'username':users [user_i].username, 'password': passwords [user_i], 'next': next}, follow=True)

			#Get Redirected back to the home page.
			self.assertTrue(response.status_code == 200)
			self.assertTrue(len(response.redirect_chain) == 1)
			self.assertTrue(response.redirect_chain[0][0] == 'http://testserver/')
			self.assertTrue(response.redirect_chain[0][1] == 302)
			self.assertTrue(response.request ['PATH_INFO'] == URL_HOME)
			client.logout()

			output_update(i + 1)
			print '\n'
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		performance_report(iteration_time)

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
UserProfileTesting: Testing for EPM User Profile Page
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class UserProfileTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all()

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all()

	def test_render_UserProfile_page(self):
		print_testing_name("test_render_UserProfile_page")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate accessing UserProfile pages.
		(users, passwords, clients) = create_test_view_setup(create_petreports=False)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()
			user_i = random.randrange(0, NUMBER_OF_TESTS)
			client_i = random.randrange(0, NUMBER_OF_TESTS)
			user = users [user_i]
			client = clients [client_i]

			print "[INFO]:%s logs onto %s to render the profile page..." % (user, client)

			loggedin = client.login(username = users [user_i].username, password = passwords[user_i])
			self.assertTrue(loggedin == True)
			response = client.get(URL_USERPROFILE + str(user.id) + '/')

			self.assertTrue(response.status_code == 200)
			#We should have the base.html -> index.html -> userprofile.html
			self.assertTrue(len(response.templates) == 3)

			client.logout()
			output_update(i + 1)
			print "\n"
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		performance_report(iteration_time)


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
LoggingTesting: Testing for EPM Logging Activities
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class LoggingTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all()

	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all()

	def test_log_account_creations(self):
		print_testing_name("test_log_account_creations")
		iteration_time = 0.00

		for i in range(NUMBER_OF_TESTS):
			start_time = time.clock()
			(user, password) = create_random_User(i, pretty_name=True)
			user_log_filename = ACTIVITY_LOG_DIRECTORY + user.username + ".log"

			with open(user_log_filename, 'r') as logger:

				lines = list(iter(logger.readlines()))
				print lines
				self.assertTrue(logging.activity_has_been_logged(ACTIVITY_ACCOUNT_CREATED, user.get_profile()) == True)
				self.assertEquals(len(lines), 1)

			logger.close()
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)	
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		performance_report(iteration_time)		


	def test_log_submit_PetReport(self):
		print_testing_name("test_log_submit_PetReport")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, passwords, clients) = create_test_view_setup(create_petreports=False)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, NUMBER_OF_TESTS)
			client_i = random.randrange(0, NUMBER_OF_TESTS)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print "[INFO]:%s logs onto %s to enter the pet report form..." % (user, client)

			#Go to the Pet Report Form Page
			response = client.get(URL_SUBMIT_PETREPORT)

			#Create and submit a Pet Report object as form content
			pr = create_random_PetReport(users [user_i])

			#Note here that we convert the PetReport attributes into a dictionary in order to pass it into the POST request object.
			pr_dict = model_to_dict(pr) 
			pr_dict ['img_path'] = None #Nullify the img_path attribute
			pr_dict ['pet_name'] = user.username + str(i)
			form  = PetReportForm() #Create an unbound form
			post = {'form': form}
			post.update(pr_dict)

			#Make the POST request Call
			response = client.post(URL_SUBMIT_PETREPORT, post, follow=True)

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertTrue(len(response.redirect_chain) == 1) 
			self.assertTrue(response.redirect_chain[0][0] == 'http://testserver/')
			self.assertEquals(response.redirect_chain[0][1], 302)
			self.assertTrue(response.request ['PATH_INFO'] == URL_HOME)
			self.assertTrue(len(PetReport.objects.all()) == 2*i + 2)
			client.logout()

			#Now, check if the activity for submitting a PetReport appears in this user's log.
			user_log_filename = ACTIVITY_LOG_DIRECTORY + user.username + ".log"
			petreport = PetReport.objects.get(proposed_by = user, pet_name = user.username + str(i))

			with open(user_log_filename, 'r') as logger:

				lines = list(iter(logger.readlines()))
				print lines
				self.assertTrue(logging.activity_has_been_logged(ACTIVITY_PETREPORT_SUBMITTED, user.get_profile(), petreport=petreport) == True)

			logger.close()			
			output_update(i + 1)
			print "\n"
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		self.assertTrue(len(PetReport.objects.all()) == 2*NUMBER_OF_TESTS) 
		performance_report(iteration_time)


	def test_log_propose_PetMatch (self):
		print_testing_name("test_log_propose_PetMatch")
		iteration_time = 0.00
		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		(users, passwords, clients, petreports) = create_test_view_setup(create_petreports=True)

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#indexes
			user_i = random.randrange(0, NUMBER_OF_TESTS)
			client_i = random.randrange(0, NUMBER_OF_TESTS)
			petreport_i = random.randrange(0, NUMBER_OF_TESTS)

			#objects
			user = users [user_i]
			password = passwords [user_i]
			client = clients [client_i]
			petreport = petreports [petreport_i]

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print "[INFO]:%s logs onto %s to enter the matching interface..." % (user, client)			

			#Go to the matching interface
			matching_url = URL_MATCHING + str(petreport.id) + "/"
			response = client.get(matching_url)
			#Generate the PetReport filters for this target PetReport so we take care of the case where there are NO PetReports to match! (causes a 302)
			filtered_pet_reports = PetReport.objects.all().exclude(pk=petreport.id).exclude(status = petreport.status).filter(pet_type = petreport.pet_type)
			if len(filtered_pet_reports) == 0:
				self.assertEquals(response.status_code, 302)
				print "[INFO]: Oh! There are no PetReports to match this PetReport with - Back to the Home Page!"
				continue

			self.assertEquals(response.status_code, 200)
			print "[INFO]:%s has successfully requested page '%s'..." % (user, matching_url) 
			candidate_petreport = random.choice(filtered_pet_reports) 

			#Go to the propose match dialog
			propose_match_url = URL_PROPOSE_MATCH + str(petreport.id) + "/" + str(candidate_petreport.id) + "/"
			response = client.get(propose_match_url)
			print "[INFO]:%s has successfully requested page '%s'..." % (user, propose_match_url) 

			#Make the POST request Call		
			description = generate_lipsum_paragraph(500)
			post = {'description': description}
			response = client.post(propose_match_url, post, follow=True)
			client.logout()						

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(len(response.redirect_chain), 1)
			self.assertEquals(response.redirect_chain[0][0], 'http://testserver/')
			self.assertEquals(response.redirect_chain[0][1], 302)
			self.assertEquals(response.request ['PATH_INFO'], URL_HOME)		

			#Now, check if the activity for proposing a PetMatch appears in this user's log.
			user_log_filename = ACTIVITY_LOG_DIRECTORY + user.username + ".log"

			with open(user_log_filename, 'r') as logger:
				#Grab the PetMatch that has either been posted in the past or has been posted by this User.
				match = PetMatch.get_PetMatch(petreport, candidate_petreport)
				print match

				if match.UserProfile_has_voted(user.get_profile()) == UPVOTE:
					print "[INFO]:A PetMatch already exists with these two PetReports, and so %s has up-voted this match!" % (user)
					self.assertTrue(logging.activity_has_been_logged(ACTIVITY_PETMATCH_UPVOTE, user.get_profile(), petmatch=match) == True)

				else:
					print "[INFO]:%s has successfully POSTED a new match!" % (user)
					self.assertTrue(logging.activity_has_been_logged(ACTIVITY_PETMATCH_PROPOSED, user.get_profile(), petmatch=match) == True)					

			logger.close()			
			output_update(i + 1)
			print "\n"
			end_time = time.clock()
			iteration_time += (end_time - start_time)		

		print ''
		performance_report(iteration_time)		

















