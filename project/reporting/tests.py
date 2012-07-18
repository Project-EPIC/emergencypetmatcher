from home.models import *
from django.contrib.auth import authenticate
from django.test.client import Client
from django.forms.models import model_to_dict
import unittest, string, random, sys, time
import test_utils as utils

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
ReportingTesting: Testing for EPM Pet Reporting
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class ReportingTesting (unittest.TestCase):

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

	def test_submit_good_PetReport(self):
		print '>>>> Testing test_submit_good_PetReport for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		clients = [ None for i in range (utils.NUMBER_OF_TESTS) ]
		users = [ None for i in range (utils.NUMBER_OF_TESTS) ]
		passwords = [ None for i in range (utils.NUMBER_OF_TESTS) ]
		user_count = 0
		client_count = 0

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()
			user_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			client_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			user = users [user_i]
			client = clients [client_i]

			if user is None:
				user, password = utils.create_random_User(i, pretty_name=True)
				users [user_i] = user
				passwords [user_i] = password
				user_count += 1

			if client is None:
				client = Client (enforce_csrf_checks=False)
				clients [client_i] = client
				client_count += 1

			print "\n%s logs onto %s to create a pet report..." % (user, client)

			#Log in First.
			loggedin = client.login(username = users [user_i].username, password = passwords[user_i])
			self.assertTrue(loggedin == True)

			#Go to the Pet Report Page
			response = client.get(utils.TEST_SUBMIT_PETREPORT_URL)
			self.assertTrue(response.status_code == 200)
			self.assertTrue(response.request ['PATH_INFO'] == utils.TEST_SUBMIT_PETREPORT_URL)
			#We should have the base.html -> index.html -> petreport_form.html
			self.assertTrue(len(response.templates) == 3)

			#Create and submit a Pet Report object as form content
			pr = utils.create_random_PetReport(users [user_i])
			#Note here that we convert the PetReport attributes into a dictionary in order to pass it into the POST request object.
			pr_dict = model_to_dict(pr) 
			pr_dict ['img_path'] = None #Nullify the img_path attribute
			form  = PetReportForm() #Create an unbound form
			post = {'form': form}
			post.update(pr_dict)

			#Make the POST request Call
			response = client.post(utils.TEST_SUBMIT_PETREPORT_URL, post, follow=True)
			client.logout()

			#Make assertions
			self.assertTrue(response.status_code == 200)
			self.assertTrue(len(response.redirect_chain) == 1)
			self.assertTrue(response.redirect_chain[0][0] == 'http://testserver/')
			self.assertTrue(response.redirect_chain[0][1] == 302)
			self.assertTrue(response.request ['PATH_INFO'] == utils.TEST_HOME_URL)
			self.assertTrue(len(User.objects.all()) == user_count)
			self.assertTrue(len(UserProfile.objects.all()) == user_count)
			self.assertTrue(len(PetReport.objects.all()) == 2*i + 2)
			utils.output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		self.assertTrue(len(UserProfile.objects.all()) <= utils.NUMBER_OF_TESTS and user_count <= utils.NUMBER_OF_TESTS)	
		self.assertTrue(len(User.objects.all()) <= utils.NUMBER_OF_TESTS)	
		self.assertTrue(len(PetReport.objects.all()) == 2*utils.NUMBER_OF_TESTS)
		utils.performance_report(iteration_time)


	def test_submit_bad_PetReport(self):
		print '>>>> Testing test_submit_bad_PetReport for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		clients = [ None for i in range (utils.NUMBER_OF_TESTS) ]
		users = [ None for i in range (utils.NUMBER_OF_TESTS) ]
		passwords = [ None for i in range (utils.NUMBER_OF_TESTS) ]
		user_count = 0
		client_count = 0

		for i in range (utils.NUMBER_OF_TESTS):
			start_time = time.clock()
			user_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			client_i = random.randrange(0, utils.NUMBER_OF_TESTS)
			user = users [user_i]
			client = clients [client_i]

			if user is None:
				user, password = utils.create_random_User(i, pretty_name=True)
				users [user_i] = user
				passwords [user_i] = password
				user_count += 1

			if client is None:
				client = Client (enforce_csrf_checks=False)
				clients [client_i] = client
				client_count += 1

			print "\n%s logs onto %s to create a pet report..." % (user, client)

			#Log in First.
			loggedin = client.login(username = users [user_i].username, password = passwords[user_i])
			self.assertTrue(loggedin == True)

			#Go to the Pet Report Page
			response = client.get(utils.TEST_SUBMIT_PETREPORT_URL)
			self.assertTrue(response.status_code == 200)
			self.assertTrue(response.request ['PATH_INFO'] == utils.TEST_SUBMIT_PETREPORT_URL)
			#We should have the base.html -> index.html -> petreport_form.html
			self.assertTrue(len(response.templates) == 3)

			#Create and submit a Pet Report object as form content
			pr = utils.create_random_PetReport(users [user_i])
			#Note here that we convert the PetReport attributes into a dictionary in order to pass it into the POST request object.
			pr_dict = model_to_dict(pr)

			#Generate bad input
			if i %2 == 0:
				pr_dict ['sex'] = utils.generate_string(5)
			elif i%3 == 0:
				pr_dict ['size'] = utils.generate_string(10)
			elif i%5 == 0:
				pr_dict ['status'] = utils.generate_string(5)
			else:
				pr_dict ['date_lost_or_found'] = 100

			pr_dict ['img_path'] = None #Nullify the img_path attribute
			form  = PetReportForm() #Create an unbound form
			post = {'form': form}
			post.update(pr_dict)

			#Make the POST request Call
			response = client.post(utils.TEST_SUBMIT_PETREPORT_URL, post, follow=True)
			client.logout()

			#Make assertions
			self.assertTrue(response.status_code == 200)
			self.assertTrue(response.request ['PATH_INFO'] == utils.TEST_SUBMIT_PETREPORT_URL)
			self.assertTrue(len(User.objects.all()) == user_count)
			self.assertTrue(len(UserProfile.objects.all()) == user_count)
			self.assertTrue(len(PetReport.objects.all()) == i + 1)
			utils.output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		self.assertTrue(len(UserProfile.objects.all()) <= utils.NUMBER_OF_TESTS and user_count <= utils.NUMBER_OF_TESTS)	
		self.assertTrue(len(User.objects.all()) <= utils.NUMBER_OF_TESTS)	
		self.assertTrue(len(PetReport.objects.all()) == utils.NUMBER_OF_TESTS)
		utils.performance_report(iteration_time)

