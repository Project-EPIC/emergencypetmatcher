from django.contrib.auth import authenticate
from django.test.client import Client
from django.forms.models import model_to_dict
from constants import *
from utils import *
from home.models import *
from pprint import pprint
import unittest, string, random, sys, time

'''===================================================================================
ReportingTesting: Testing for EPM Pet Reporting
==================================================================================='''
class ReportingTesting (unittest.TestCase):

	#Get rid of all objects in the QuerySet.
	def setUp(self):
		delete_all(leave_Users=False)
	#Get rid of all objects in the QuerySet.
	def tearDown(self):
		delete_all(leave_Users=False)

	def test_get_PetReport_form(self):
		print_testing_name("test_get_PetReport_form")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects()
		users = results["users"]
		clients = results["clients"]

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print_test_msg("%s logs onto %s to enter the pet report form..." % (user, client))

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
		performance_report(iteration_time)


	def test_post_good_PetReport(self):
		print_testing_name("test_post_good_PetReport")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects()
		users = results["users"]
		clients = results["clients"]

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print_test_msg("%s logs onto %s to enter the pet report form..." % (user, client))

			#Go to the Pet Report Form Page
			response = client.get(URL_SUBMIT_PETREPORT)

			#Create and submit a Pet Report object as form content
			pr = create_random_PetReport(user=user, save=False)

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
			self.assertTrue(len(PetReport.objects.all()) == i + 1)
			client.logout()

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS) 
		performance_report(iteration_time)


	def test_post_bad_PetReport(self):
		print_testing_name("test_post_bad_PetReport")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects()
		users = results["users"]
		clients = results["clients"]

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print_test_msg("%s logs onto %s to enter the pet report form..." % (user, client))

			#Go to the Pet Report Form Page
			response = client.get(URL_SUBMIT_PETREPORT)

			#Create and submit a Pet Report object as form content
			pr = create_random_PetReport(user=user, save=False)
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
			self.assertTrue(len(PetReport.objects.all()) == 0)
			client.logout()
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		self.assertTrue(len(PetReport.objects.all()) == 0)
		performance_report(iteration_time)


	def test_post_different_image_formats_for_PetReports(self):
		print_testing_name("test_post_different_image_formats_for_PetReports")
		iteration_time = 0.00

		#Need this to randomly choose the PetReport image we're going to use.
		#Look in the test_images and append all images to the images list to do this.
		images = []
		saved_images = []		

		for f in os.listdir(PETREPORT_IMAGES_DIFFERENT_FORMATS_DIRECTORY):
			if f != ".DS_Store" and f != ".anchor":
				images.append(PETREPORT_IMAGES_DIFFERENT_FORMATS_DIRECTORY + f)

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects()
		users = results["users"]
		clients = results["clients"]

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print_test_msg("%s logs onto %s to enter the pet report form..." % (user, client))

			#Note here that we convert the PetReport attributes into a dictionary in order to pass it into the POST request object.
			petreport = create_random_PetReport(user=user, save=False)
			pr_dict = model_to_dict(petreport)

			#Randomly choose the image path to use for this request.
			image = random.choice(images)
			print_test_msg("%s will use the file '%s' for a new PetReport submission." % (user.username, image))
			image_file = open(image, "rb") #Need to specify "reading (r) a binary (b) file"
			pr_dict ['img_path'] = image_file
			form  = PetReportForm() #Create an unbound form
			post = {'form': form}
			post.update(pr_dict)
			petreport.img_path = image_file
			petreport.thumb_path = image_file

			#Make the POST request Call
			response = client.post(URL_SUBMIT_PETREPORT, post, follow=True)
			image_file.close()

			#Get the new PetReport created with new image file path.
			new_petreport = PetReport.objects.get(pk=i + 1)
			#Just grab the name of the file, nothing else.
			img_name = new_petreport.img_path.name.split("/")[2]

			#Make assertions
			self.assertEquals(petreport.status, new_petreport.status)
			self.assertEquals(petreport.pet_type, new_petreport.pet_type)
			self.assertEquals(petreport.pet_name, new_petreport.pet_name)
			#Assert that PetReport name is found in the img_path and thumb_path name.
			self.assertTrue(petreport.pet_name in new_petreport.img_path.name)
			self.assertTrue(petreport.pet_name in new_petreport.thumb_path.name)
			#Assert that PetReport Status is found in the img_path and thumb_path name.
			self.assertTrue(petreport.status in new_petreport.img_path.name)
			self.assertTrue(petreport.status in new_petreport.thumb_path.name)					
			#Assert that PetReport UserProfile username  is found in the img_path and thumb_path name.
			self.assertTrue(petreport.proposed_by.user.username in new_petreport.img_path.name)
			self.assertTrue(petreport.proposed_by.user.username in new_petreport.thumb_path.name)		

			self.assertEquals(response.status_code, 200)
			self.assertTrue(len(response.redirect_chain) == 1) 
			self.assertTrue(response.redirect_chain[0][0] == 'http://testserver/')
			self.assertEquals(response.redirect_chain[0][1], 302)
			self.assertTrue(response.request ['PATH_INFO'] == URL_HOME)
			client.logout()

			#Add the img name to this saved images list for future deletion.
			saved_images.append(img_name)
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS)
		performance_report(iteration_time)
		#Delete the test images created here in the petreport_images folder.
		delete_PetReport_images(from_list=saved_images)


	def test_check_PetReport_image_and_thumbnail(self):
		print_testing_name("test_check_PetReport_image_and_thumbnail")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate posting of PetReport objects.
		results = setup_objects()
		users = results["users"]
		clients = results["clients"]

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print_test_msg("%s logs onto %s to enter the pet report form..." % (user, client))

			#Go to the Pet Report Form Page
			response = client.get(URL_SUBMIT_PETREPORT)

			#Create (but do not save) a random Pet Report object.
			petreport = create_random_PetReport(save=False, user=user)

			#We are testing this functionality: Save the img_path and thumb_path PetReport attributes.
			petreport.set_images(petreport.img_path, save=True)
			#At this point, we're supposed to have two images related to the submitted PetReport.

			#The thumbnail Check
			expected_thumbnail = PETREPORT_THUMBNAILS_DIRECTORY + str(petreport.proposed_by.id) + "-" + petreport.proposed_by.user.username + "-" + str(petreport.id) + "-" + petreport.pet_name + "-" + petreport.status + ".jpg"
			print_test_msg ("Expected Thumbnail Path: " + expected_thumbnail)
			self.assertTrue(os.path.exists(expected_thumbnail) == True)
			print_success_msg ("Expected and Actual Thumbnail paths match.")

			#The actual image Check
			expected_img = PETREPORT_IMAGES_DIRECTORY + str(petreport.proposed_by.id) + "-" + petreport.proposed_by.user.username + "-" + str(petreport.id) + "-" + petreport.pet_name + "-" + petreport.status + ".jpg"
			print_test_msg ("Expected Image Path: " + expected_img)
			self.assertTrue(os.path.exists(expected_img) == True)
			print_success_msg ("Expected and Actual Image paths match.")

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)

		self.assertTrue(len(UserProfile.objects.all()) <= NUMBER_OF_TESTS)
		self.assertTrue(len(User.objects.all()) <= NUMBER_OF_TESTS)	
		self.assertTrue(len(PetReport.objects.all()) == NUMBER_OF_TESTS)
		performance_report(iteration_time)

	def test_get_PetReport_detailed_page(self):
		print_testing_name("test_get_PetReport_detailed_page")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords and petreports 
		results = setup_objects(create_petreports=True)
		users = results["users"]
		clients = results["clients"]
		petreports = results["petreports"]

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)
			petreport = random.choice(petreports)
			prdp_url = URL_PRDP + str(petreport.id) + "/"

			#Test without logger in First.
			print_test_msg("Getting PRDP from %s without being logged in" % (client))
			response = client.get(prdp_url)
			self.assertEquals(response.status_code, 200)
			self.assertTrue(response.request ['PATH_INFO'] == prdp_url)

			#Log in
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)
			print_test_msg("%s logs onto %s to EPM" % (user, client))

			#Test after logger in.
			response = client.get(prdp_url)
			self.assertEquals(response.status_code, 200)
			self.assertTrue(response.request ['PATH_INFO'] == prdp_url)

			#Test navigation to user profiles of all workers
			for worker in petreport.workers.all():
				worker_url = URL_USERPROFILE +str(worker.user.id)+ "/"
				response = client.get(worker_url)
				self.assertEquals(response.status_code, 200)
				self.assertTrue(response.request ['PATH_INFO'] == worker_url)

			print_test_msg("[OK]:Navigation to all workers' user profiles is successful")

			expected_status_code = 200
			all_pet_reports = PetReport.objects.all().exclude(pk=petreport.id)
    		filtered_pet_reports = all_pet_reports.exclude(status = petreport.status).filter(pet_type = petreport.pet_type)
	        if len(filtered_pet_reports) == 0:
	        	expected_status_code = 302	

			#Test navigation to the matching interface
			matching_url = URL_MATCHING + str(petreport.id)+ "/"
			response = client.get(matching_url)
			self.assertEquals(response.status_code, expected_status_code) 
			self.assertTrue(response.request ['PATH_INFO'] == matching_url)
			print_test_msg("[OK]:Navigation to the matching interface is successful")

			client.logout()
			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)

	def test_add_PetReport_bookmark(self):
		print_testing_name("test_add_PetReport_bookmark")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate bookmarking of PetReport objects.
		results = setup_objects(create_petreports=True)
		users = results["users"]
		clients = results["clients"]
		petreports = results["petreports"]

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)
			petreport = random.choice(petreports)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)			
			print_test_msg("%s logs onto %s to enter the PRDP..." % (user, client))

			prdp_url = URL_PRDP + str(petreport.id) + "/"
			print_test_msg(prdp_url)
			response = client.get(prdp_url)
			old_bookmarks_count = user.get_profile().bookmarks_related.count()

			#if user has bookmarked this petreport previously,
			if(petreport.UserProfile_has_bookmarked(user.get_profile())):
				previously_bookmarked = True
			else:
				previously_bookmarked = False

			add_bookmark_url = URL_BOOKMARK_PETREPORT
			post =  {"petreport_id":petreport.id, "user_id":user.id, "action":"Bookmark this Pet"}
			response = client.post(add_bookmark_url, post, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)
			new_bookmarks_count = user.get_profile().bookmarks_related.count()

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], add_bookmark_url)
			self.assertTrue(petreport.UserProfile_has_bookmarked(user.get_profile()))
			self.assertEquals(petreport.bookmarked_by.get(pk = user.id), user.get_profile())
			if(not previously_bookmarked):
				self.assertEquals(old_bookmarks_count, (new_bookmarks_count-1))

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)	

	def test_remove_PetReport_bookmark(self):
		print_testing_name("test_remove_PetReport_bookmark")
		iteration_time = 0.00

		#Need to setup clients, users, and their passwords in order to simulate bookmarking of PetReport objects.
		results = setup_objects(create_petreports=True)
		users = results["users"]
		clients = results["clients"]
		petreports = results["petreports"]

		for i in range (NUMBER_OF_TESTS):
			start_time = time.clock()

			#objects
			user, password = random.choice(users)
			client = random.choice(clients)
			petreport = random.choice(petreports)

			#Log in First.
			loggedin = client.login(username = user.username, password = password)
			self.assertTrue(loggedin == True)			
			print_test_msg("%s logs onto %s to enter the PRDP..." % (user, client))

			#navigate to the prdp
			prdp_url = URL_PRDP + str(petreport.id) + "/"
			print_test_msg(prdp_url)
			response = client.get(prdp_url)

			#add a bookmark
			add_bookmark_url = URL_BOOKMARK_PETREPORT
			post =  {"petreport_id":petreport.id, "user_id":user.id,"action":"Bookmark this Pet"}
			response = client.post(add_bookmark_url, post, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)
			old_bookmarks_count = user.get_profile().bookmarks_related.count()

			#remove the bookmark
			remove_bookmark_url = URL_BOOKMARK_PETREPORT
			post =  {"petreport_id":petreport.id, "user_id":user.id,"action":"Remove Bookmark"}
			response = client.post(remove_bookmark_url, post, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)
			new_bookmarks_count = user.get_profile().bookmarks_related.count()

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], remove_bookmark_url)
			#self.assertTrue(petreport.UserProfile_has_bookmarked(user.get_profile()),False)
			self.assertEquals(old_bookmarks_count, (new_bookmarks_count+1))

			#add back the bookmark
			add_bookmark_url = URL_BOOKMARK_PETREPORT
			post =  {"petreport_id":petreport.id, "user_id":user.id,"action":"Bookmark this Pet"}
			response = client.post(add_bookmark_url, post, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)
			old_bookmarks_count = user.get_profile().bookmarks_related.count()


			#remove the bookmark 
			remove_bookmark_url = URL_BOOKMARK_PETREPORT
			post =  {"petreport_id":petreport.id, "user_id":user.id,"action":"Remove Bookmark"}
			response = client.post(add_bookmark_url, post, HTTP_X_REQUESTED_WITH='XMLHttpRequest', follow=True)
			new_bookmarks_count = user.get_profile().bookmarks_related.count()

			#Make assertions
			self.assertEquals(response.status_code, 200)
			self.assertEquals(response.request ['PATH_INFO'], remove_bookmark_url)
			#self.assertTrue(petreport.UserProfile_has_bookmarked(user.get_profile()),False)
			self.assertEquals(old_bookmarks_count, (new_bookmarks_count+1))

			output_update(i + 1)
			end_time = time.clock()
			iteration_time += (end_time - start_time)
		performance_report(iteration_time)	




			