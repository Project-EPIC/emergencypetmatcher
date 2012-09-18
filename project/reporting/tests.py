from django.contrib.auth import authenticate
from django.test.client import Client
from django.forms.models import model_to_dict
from constants import *
from utils import *
from home.models import *
import unittest, string, random, sys, time


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

	def test_get_petreport_form(self):
		print '>>>> Testing test_get_petreport_form for %d iterations' % NUMBER_OF_TESTS
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
			print "\n%s logs onto %s to enter the pet report form..." % (user, client)

			#Go to the Pet Report Form Page
			response = client.get(URL_SUBMIT_PETREPORT)
			self.assertTrue(response.status_code == 200)
			self.assertTrue(response.request ['PATH_INFO'] == URL_SUBMIT_PETREPORT)
			#We should have the base.html -> index.html -> petreport_form.html
			self.assertTrue(len(response.templates) == 3)

			client.logout()

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		performance_report(iteration_time)


	def test_post_good_PetReport(self):
		print '>>>> Testing test_post_good_PetReport for %d iterations' % NUMBER_OF_TESTS
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
			print "\n%s logs onto %s to enter the pet report form..." % (user, client)

			#Go to the Pet Report Form Page
			response = client.get(URL_SUBMIT_PETREPORT)

			#Create and submit a Pet Report object as form content
			pr = create_random_PetReport(users [user_i])

			#Note here that we convert the PetReport attributes into a dictionary in order to pass it into the POST request object.
			pr_dict = model_to_dict(pr) 
			pr_dict ['img_path'] = None #Nullify the img_path attribute
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

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		self.assertTrue(len(UserProfile.objects.all()) <= utils.NUMBER_OF_TESTS)
		self.assertTrue(len(User.objects.all()) <= utils.NUMBER_OF_TESTS)	
		self.assertTrue(len(PetReport.objects.all()) == 2*utils.NUMBER_OF_TESTS) 
		utils.performance_report(iteration_time)


	def test_post_bad_PetReport(self):
		print '>>>> Testing test_post_bad_PetReport for %d iterations' % NUMBER_OF_TESTS
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
			print "\n%s logs onto %s to enter the pet report form..." % (user, client)

			#Go to the Pet Report Form Page
			response = client.get(URL_SUBMIT_PETREPORT)

			#Create and submit a Pet Report object as form content
			pr = create_random_PetReport(users [user_i])
			#Note here that we convert the PetReport attributes into a dictionary in order to pass it into the POST request object.
			pr_dict = model_to_dict(pr)

			#Generate bad input
			if i %2 == 0:
				pr_dict ['sex'] = generate_string(5)
			elif i%3 == 0:
				pr_dict ['size'] = generate_string(10)
			elif i%5 == 0:
				pr_dict ['status'] = generate_string(5)
			else:
				pr_dict ['date_lost_or_found'] = 100

			pr_dict ['img_path'] = None #Nullify the img_path attribute
			form  = PetReportForm() #Create an unbound form
			post = {'form': form}
			post.update(pr_dict)

			#Make the POST request Call
			response = client.post(URL_SUBMIT_PETREPORT, post, follow=True)

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertTrue(response.request ['PATH_INFO'] == URL_SUBMIT_PETREPORT)
			self.assertTrue(len(PetReport.objects.all()) == i + 1)
			client.logout()

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS)
		performance_report(iteration_time)

	def test_get_PetReport_detailed_page(self):
		print '>>>> Testing test_get_PetReport_detailedpage for %d iterations' % NUMBER_OF_TESTS
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords and petreports 
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
			prdp_url = URL_PRDP + str(petreport.id) + "/"

			#Test without logging in First.
			print "\n\nGetting PRDP from %s without being logged in" % (client)
			response = client.get(prdp_url)
			self.assertEquals(response.status_code, 200)
			self.assertTrue(response.request ['PATH_INFO'] == prdp_url)

			#Log in
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print "%s logs onto %s to EPM" % (user, client)

			#Test after Logging in.
			response = client.get(prdp_url)
			self.assertEquals(response.status_code, 200)
			self.assertTrue(response.request ['PATH_INFO'] == prdp_url)

			#Test navigation to user profiles of all workers
			for worker in petreport.workers.all():
				worker_url = URL_USERPROFILE +str(worker.user.id)+ "/"
				response = client.get(worker_url)
				self.assertEquals(response.status_code, 200)
				self.assertTrue(response.request ['PATH_INFO'] == worker_url)

			print "Navigation to all workers' user profiles is successful"

			expected_status_code = 200
			all_pet_reports = PetReport.objects.all().exclude(pk=petreport_i)
    		filtered_pet_reports = all_pet_reports.exclude(status = petreport.status).filter(pet_type = petreport.pet_type)
	        if len(filtered_pet_reports) == 0:
	        	expected_status_code = 302	

			#Test navigation to the matching interface
			matching_url = URL_MATCHING + str(petreport.id)+ "/"
			response = client.get(matching_url)
			self.assertEquals(response.status_code, expected_status_code) 
			self.assertTrue(response.request ['PATH_INFO'] == matching_url)
			print "Navigation to the matching interface is successful"

			#test navigation to the PMDP
			client.logout()

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		performance_report(iteration_time)

	def test_add_PetReport_bookmark(self):
		print '>>>> Testing test_add_PetReport_bookmark for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate bookmarking of PetReport objects.
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
			print "\n%s logs onto %s to enter the PRDP..." % (user, client)

			prdp_url = utils.TEST_PRDP_URL + str(petreport.id) + "/"
			print prdp_url
			response = client.get(prdp_url)
			old_bookmarks_count = user.get_profile().bookmarks_related.count()

			#if user has bookmarked this petreport previously,
			if(petreport.UserProfile_has_bookmarked(user.get_profile())):
				previously_bookmarked = True
			else:
				previously_bookmarked = False

			add_bookmark_url = utils.TEST_BOOKMARK_PETREPORT_URL
			post =  {"petreport_id":petreport.id, "user_id":user.id,"action":"Bookmark this Pet"}
			response = client.post(add_bookmark_url, post, follow=True)
			new_bookmarks_count = user.get_profile().bookmarks_related.count()

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], add_bookmark_url)
			self.assertTrue(petreport.UserProfile_has_bookmarked(user.get_profile()))
			self.assertEquals(petreport.bookmarked_by.get(pk = user.id), user.get_profile())
			if(not previously_bookmarked):
				self.assertEquals(old_bookmarks_count, (new_bookmarks_count-1))

			utils.output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''
		utils.performance_report(iteration_time)	

	def test_remove_petreport_bookmark(self):
		print '>>>> Testing test_add_PetReport_bookmark for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate bookmarking of PetReport objects.
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
			print "\n%s logs onto %s to enter the PRDP..." % (user, client)

			#navigate to the prdp
			prdp_url = utils.TEST_PRDP_URL + str(petreport.id) + "/"
			print prdp_url
			response = client.get(prdp_url)


			#add a bookmark
			add_bookmark_url = utils.TEST_BOOKMARK_PETREPORT_URL
			post =  {"petreport_id":petreport.id, "user_id":user.id,"action":"Bookmark this Pet"}
			response = client.post(add_bookmark_url, post, follow=True)
			old_bookmarks_count = user.get_profile().bookmarks_related.count()

			#remove the bookmark
			remove_bookmark_url = utils.TEST_BOOKMARK_PETREPORT_URL
			post =  {"petreport_id":petreport.id, "user_id":user.id,"action":"Remove Bookmark"}
			response = client.post(remove_bookmark_url, post, follow=True)
			new_bookmarks_count = user.get_profile().bookmarks_related.count()

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], remove_bookmark_url)
			#self.assertTrue(petreport.UserProfile_has_bookmarked(user.get_profile()),False)
			self.assertEquals(old_bookmarks_count, (new_bookmarks_count+1))

			#add back the bookmark
			add_bookmark_url = utils.TEST_BOOKMARK_PETREPORT_URL
			post =  {"petreport_id":petreport.id, "user_id":user.id,"action":"Bookmark this Pet"}
			response = client.post(add_bookmark_url, post, follow=True)
			old_bookmarks_count = user.get_profile().bookmarks_related.count()


			#navigate to the bookmarks page
			bookmarks_page_url = utils.TEST_BOOKMARKED_PETREPORTS_URL
			print bookmarks_page_url
			response = client.get(bookmarks_page_url)

			#remove the bookmark 
			remove_bookmark_url = utils.TEST_BOOKMARK_PETREPORT_URL
			post =  {"petreport_id":petreport.id, "user_id":user.id,"action":"Remove Bookmark"}
			response = client.post(add_bookmark_url, post, follow=True)
			new_bookmarks_count = user.get_profile().bookmarks_related.count()


			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], remove_bookmark_url)
			#self.assertTrue(petreport.UserProfile_has_bookmarked(user.get_profile()),False)
			self.assertEquals(old_bookmarks_count, (new_bookmarks_count+1))


			utils.output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		print ''

		utils.performance_report(iteration_time)	

	def test_get_bookmarks_page(self):
		print '>>>> Testing test_get_bookmarks_page for %d iterations' % utils.NUMBER_OF_TESTS
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate retrieving the bookmarks page for a user.
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
			print "\n%s logs onto %s to enter the bookmarks page..." % (user, client)

			#navigate to the bookmarks page
			bookmarks_page_url = utils.TEST_BOOKMARKED_PETREPORTS_URL
			print bookmarks_page_url
			response = client.get(bookmarks_page_url)
