from django.contrib.auth import authenticate
from django.test.client import Client
from django.test import TestCase
from time import sleep
from selenium import webdriver
from django.forms.models import model_to_dict
from fixture import *
from django.template.loader import render_to_string
from reporting.constants import PETREPORT_SAMPLES_DOG_DIRECTORY
from home.constants import *
from reporting.constants import *
from socializing.constants import *
from verifying.constants import *
from matching.constants import *
from utilities.utils import *
import string, random, sys, time, urlparse, project.settings, math, pdb

class UserProfileTesting (TestCase):
	def setUp(self):
		delete_all(leave_Users=False)
	def tearDown(self):
		delete_all(leave_Users=False)

	def test_save_UserProfile(self):
		user, password = create_random_User(0)
		username = user.username
		user_profile = user.userprofile
		user_profile.reputation = random.randint(0,100)
		user_profile.save()
		user_prof = UserProfile.objects.get(user = user)
		self.assertEquals(user_profile, user_prof)
		user = user_prof.user
		self.assertTrue(user.check_password(password) == True)
		userObject = authenticate (username = username, password = password)
		self.assertTrue(userObject is not None)

	def test_update_User (self):
		user, password = create_random_User()
		username = user.username
		user_profile = user.userprofile
		user_profile.reputation = random.randint(0,100)
		user_profile.save()
		changed_username = generate_string (10) + str(0)
		user.username = changed_username
		user.save()
		user_profile = UserProfile.objects.get(user = user)
		user = user_profile.user
		self.assertEqual (user.username, changed_username)
		self.assertNotEqual (user.username, username)
		self.assertTrue(user.check_password(password) == True)
		userObject = authenticate (username = changed_username, password = password)
		self.assertTrue(userObject is not None)

	def test_delete_User(self):
		user, password = create_random_User()
		username = user.username
		user_profile = user.userprofile
		user_profile.reputation = random.randint(0,100)
		user_profile.save()
		User.objects.get(username = username).delete()
		self.assertTrue(len(UserProfile.objects.all()) == 0)
		self.assertTrue(len(User.objects.all()) == 0)
		userObject = authenticate (username = username, password = password)
		self.assertTrue(userObject is None)


class LoginTesting (TestCase):
	def setUp(self):
		delete_all(leave_Users=False)
	def tearDown(self):
		delete_all(leave_Users=False)

	def test_login_success(self):
		user, password = create_random_User()
		client = Client (enforce_csrf_checks=False)
		#Go to the Login Page
		response = client.get(URL_LOGIN)
		next = response.context ['next']
		self.assertTrue(response.status_code == 200)
		self.assertTrue(response.request ['PATH_INFO'] == URL_LOGIN)
		self.assertTrue(next == URL_HOME)

		#Submit Login information
		response = client.post (URL_LOGIN, {'username': user.username, 'password': password, 'next': next}, follow=True)

		#Get Redirected back to the home page.
		self.assertTrue(response.status_code == 200)
		self.assertTrue(len(response.redirect_chain) == 1)
		self.assertTrue(response.redirect_chain[0][0] == 'http://testserver/')
		self.assertTrue(response.redirect_chain[0][1] == 302)
		self.assertTrue(response.request ['PATH_INFO'] == URL_HOME)
		client.logout()

	def test_login_fail(self):
		user, password = create_random_User()
		client = Client (enforce_csrf_checks=False)
		#Go to the Login Page
		response = client.get(URL_LOGIN)
		next = response.context ['next']
		self.assertTrue(response.status_code == 200)
		self.assertTrue(response.request ['PATH_INFO'] == URL_LOGIN)
		self.assertTrue(next == URL_HOME)
		#Submit Login information
		response = client.post (URL_LOGIN, {'username': user.username, 'password': "wrong-password", 'next': next}, follow=True)
		#Get Redirected back to the home page.
		self.assertTrue(response.status_code == 200)
		self.assertTrue(response.request ['PATH_INFO'] == URL_LOGIN)
		client.logout()

class ActivityTesting (TestCase):
	def setUp(self):
		delete_all(leave_Users=False)
	def tearDown(self):
		delete_all(leave_Users=False)

	def test_account_created(self):
		user = User.objects.create(username="test", email="test@test.com")
		a = Activity.objects.get(source_id=user.userprofile.id)
		self.assertTrue(a.activity == "ACTIVITY_ACCOUNT_CREATED")

	def test_login(self):
		user, pwd = create_random_User()
		client = Client (enforce_csrf_checks=False)
		response = client.get(URL_LOGIN)
		user_next = response.context ['next']
		response = client.post (URL_LOGIN, {'username': user.username, 'password': pwd, 'next':user_next}, follow=True)
		activities = Activity.objects.filter(source_id=user.userprofile.id, activity="ACTIVITY_LOGIN")
		self.assertTrue(len(activities) == 1)

	def test_logout(self):
		user, pwd = create_random_User()
		client = Client (enforce_csrf_checks=False)
		response = client.get(URL_LOGIN)
		user_next = response.context ['next']
		response = client.post (URL_LOGIN, {'username': user.username, 'password': pwd, 'next':user_next}, follow=True)
		response = client.post (URL_LOGOUT)
		activities = Activity.objects.filter(source_id=user.userprofile.id, activity="ACTIVITY_LOGOUT")
		self.assertTrue(len(activities) == 1)

	def test_user_changed_username(self):
		user, pwd = create_random_User()
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username = user.username, password = pwd)
		post = model_to_dict(user.userprofile)
		post.update({"username": "new_username", "first_name": user.first_name, "last_name": user.last_name, "email":"test@test.com"})
		response = client.post(URL_EDITUSERPROFILE_INFO, post, follow=True)
		self.assertTrue(response.status_code == 200)
		self.assertTrue(response.request ['PATH_INFO'] == URL_USERPROFILE + str(user.userprofile.id) + "/")
		activities = Activity.objects.filter(source_id=user.userprofile.id, activity="ACTIVITY_USER_CHANGED_USERNAME")
		self.assertTrue(len(activities) == 1)

	def test_user_set_photo(self):
		user, pwd = create_random_User()
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username=user.username, password=pwd)
		post = model_to_dict(user.userprofile)
		img = open(PETREPORT_SAMPLES_DOG_DIRECTORY + random.choice(os.listdir(PETREPORT_SAMPLES_DOG_DIRECTORY)), "rb")
		post.update({"username": user.username, "first_name": user.first_name, "last_name": user.last_name, "email":"test@test.com", "photo":img})
		response = client.post(URL_EDITUSERPROFILE_INFO, post, follow=True)
		self.assertTrue(response.status_code == 200)
		self.assertTrue(response.request['PATH_INFO'] == URL_USERPROFILE + str(user.userprofile.id) + "/")
		activities = Activity.objects.filter(source_id=user.userprofile.id, activity="ACTIVITY_USER_SET_PHOTO")
		self.assertTrue(len(activities) == 1)

	def test_social_follow(self):
		user1, pwd1 = create_random_User()
		user2, pwd2 = create_random_User()
		client = Client(enforce_csrf_checks=False)
		for (user, pwd, other_user) in [(user1, pwd1, user2), (user2, pwd2, user1)]:
			loggedin = client.login(username=user.username, password=pwd)
			response = client.post(URL_FOLLOW, {"target_userprofile_id": other_user.userprofile.id}, follow=True)
			self.assertTrue(response.status_code == 200)
			self.assertTrue(response.request['PATH_INFO'] == URL_USERPROFILE + str(other_user.userprofile.id) + "/")
			activities = Activity.objects.filter(userprofile=user.userprofile, activity="ACTIVITY_SOCIAL_FOLLOW")
			self.assertTrue(len(activities) == 1)

	def test_social_unfollow(self):
		user1, pwd1 = create_random_User()
		user2, pwd2 = create_random_User()
		client = Client(enforce_csrf_checks=False)
		for (user, pwd, other_user) in [(user1, pwd1, user2), (user2, pwd2, user1)]:
			loggedin = client.login(username=user.username, password=pwd)
			response = client.post(URL_FOLLOW, {"target_userprofile_id": other_user.userprofile.id}, follow=True)
		for (user, pwd, other_user) in [(user1, pwd1, user2), (user2, pwd2, user1)]:
			loggedin = client.login(username=user.username, password=pwd)
			response = client.post(URL_UNFOLLOW, {"target_userprofile_id": other_user.userprofile.id}, follow=True)
			activities = Activity.objects.filter(userprofile=user.userprofile, activity="ACTIVITY_SOCIAL_UNFOLLOW")
			self.assertTrue(len(activities) == 1)

	def test_send_message_to_user(self):
		user1, pwd1 = create_random_User()
		user2, pwd2 = create_random_User()
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username=user1.username, password=pwd1)
		response = client.post(URL_SEND_MESSAGE_TO_USER, {"target_userprofile_id": user2.userprofile.id, "message": "Sample Message"}, follow=True)
		self.assertTrue(response.status_code == 200)
		self.assertTrue(response.request['PATH_INFO'] == URL_USERPROFILE + str(user2.userprofile.id) + "/")
		activities = Activity.objects.filter(userprofile=user1.userprofile, activity="ACTIVITY_SOCIAL_SEND_MESSAGE_TO_USER")
		self.assertTrue(len(activities) == 1)

	def test_petreport_submitted(self):
		user, pwd = create_random_User()
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username = user.username, password = pwd)
		pr = create_random_PetReport(user=user, save=False)
		pr_dict = model_to_dict(pr)
		form  = PetReportForm()
		settings.RECAPTCHA_SERVER_SECRET=settings.TEST_RECAPTCHA_SERVER_SECRET
		post = {'form': form, "g-recaptcha-response":settings.TEST_RECAPTCHA_CLIENT_SECRET}
		post.update(pr_dict)
		response = client.post(URL_SUBMIT_PETREPORT, post, follow=True)
		activities = Activity.objects.filter(userprofile=user.userprofile, activity="ACTIVITY_PETREPORT_SUBMITTED")
		self.assertTrue(len(activities) == 1)

	def test_petreport_bookmark(self):
		user1, pwd1 = create_random_User()
		pr1 = create_random_PetReport(user=user1)
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username=user1.username, password=pwd1)
		response = client.post(URL_BOOKMARK_PETREPORT, {"petreport_id":pr1.id, "action":"Bookmark this Pet"}, HTTP_X_REQUESTED_WITH="XMLHttpRequest", follow=True)
		activities = Activity.objects.filter(userprofile=user1.userprofile, source_id=pr1.id, activity="ACTIVITY_PETREPORT_ADD_BOOKMARK")
		self.assertTrue(len(activities) == 1)
		response = client.post(URL_BOOKMARK_PETREPORT, {"petreport_id":pr1.id, "action":"Remove Bookmark"}, HTTP_X_REQUESTED_WITH="XMLHttpRequest", follow=True)
		activities = Activity.objects.filter(userprofile=user1.userprofile, source_id=pr1.id, activity="ACTIVITY_PETREPORT_REMOVE_BOOKMARK")
		self.assertTrue(len(activities) == 1)

	def test_petmatch_proposed (self):
		user1, pwd1 = create_random_User()
		user2, pwd2 = create_random_User()
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username=user1.username, password=pwd1)
		pr1 = create_random_PetReport(user=user1, status="Lost", pet_type="Dog")
		pr2 = create_random_PetReport(user=user2, status="Found", pet_type="Dog")
		settings.RECAPTCHA_SERVER_SECRET=settings.TEST_RECAPTCHA_SERVER_SECRET
		post = {"g-recaptcha-response": settings.TEST_RECAPTCHA_CLIENT_SECRET}
		response = client.post(URL_PROPOSE_PETMATCH + "%d/%d/" % (pr1.id, pr2.id), post, follow=True)
		activities = Activity.objects.filter(userprofile=user1.userprofile, activity="ACTIVITY_PETMATCH_PROPOSED")
		self.assertEquals(response.request ['PATH_INFO'], URL_HOME)
		self.assertTrue(len(activities) == 1)

	def test_petmatch_vote(self):
		user1, pwd1 = create_random_User()
		user2, pwd2 = create_random_User()
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username=user1.username, password=pwd1)
		pr1 = create_random_PetReport(user=user1, status="Lost", pet_type="Dog")
		pr2 = create_random_PetReport(user=user2, status="Found", pet_type="Dog")
		pm = PetMatch.objects.create(lost_pet=pr1, found_pet=pr2, proposed_by=user1.userprofile)
		response = client.post(URL_VOTE_PETMATCH + str(pm.id), {"vote":"upvote"}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
		activities = Activity.objects.filter(userprofile=user1.userprofile, source_id=pm.id, activity="ACTIVITY_PETMATCH_UPVOTE")
		self.assertTrue(len(activities) == 1)
		PetMatchCheck.objects.all().delete()
		response = client.post(URL_VOTE_PETMATCH + str(pm.id), {"vote":"downvote"}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
		activities = Activity.objects.filter(userprofile=user1.userprofile, source_id=pm.id, activity="ACTIVITY_PETMATCH_DOWNVOTE")
		self.assertTrue(len(activities) == 1)

	def test_petmatchcheck_verify(self):
		user1, pwd1 = create_random_User()
		user2, pwd2 = create_random_User()
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username=user1.username, password=pwd1)
		pr1 = create_random_PetReport(user=user1, status="Lost", pet_type="Dog")
		pr2 = create_random_PetReport(user=user2, status="Found", pet_type="Dog")
		pm = PetMatch.objects.create(lost_pet=pr1, found_pet=pr2, proposed_by=user1.userprofile)
		response = client.post(URL_VOTE_PETMATCH + "%d/" % (pm.id), {"vote":"upvote"}, follow=True)
		activities = Activity.objects.filter(userprofile=user1.userprofile, source_id=PetMatchCheck.objects.get().id, activity="ACTIVITY_PETMATCHCHECK_VERIFY")
		self.assertTrue(len(activities) == 1)

	def test_petmatchcheck_verify_success(self):
		user1, pwd1 = create_random_User()
		user2, pwd2 = create_random_User()
		client = Client(enforce_csrf_checks=False)
		pr1 = create_random_PetReport(user=user1, status="Lost", pet_type="Dog")
		pr2 = create_random_PetReport(user=user2, status="Found", pet_type="Dog")
		pm = PetMatch.objects.create(lost_pet=pr1, found_pet=pr2, proposed_by=user1.userprofile)
		pmc = PetMatchCheck.objects.create(petmatch=pm)
		loggedin = client.login(username=user1.username, password=pwd1)
		response = client.post(URL_VERIFY_PETMATCHCHECK + str(pmc.id) + "/", {"verify-choice":"1"}, follow=True)
		activities = Activity.objects.filter(userprofile=user1.userprofile, activity="ACTIVITY_PETMATCHCHECK_VERIFY_SUCCESS")
		self.assertTrue(len(activities) == 0)
		loggedin = client.login(username=user2.username, password=pwd2)
		response = client.post(URL_VERIFY_PETMATCHCHECK + str(pmc.id) + "/", {"verify-choice":"1"}, follow=True)
		activities = Activity.objects.filter(userprofile=user1.userprofile, activity="ACTIVITY_PETMATCHCHECK_VERIFY_SUCCESS")
		self.assertTrue(len(activities) == 1)

	def test_petmatchcheck_verify_fail(self):
		user1, pwd1 = create_random_User()
		user2, pwd2 = create_random_User()
		client = Client(enforce_csrf_checks=False)
		pr1 = create_random_PetReport(user=user1, status="Lost", pet_type="Dog")
		pr2 = create_random_PetReport(user=user2, status="Found", pet_type="Dog")
		pm = PetMatch.objects.create(lost_pet=pr1, found_pet=pr2, proposed_by=user1.userprofile)
		pmc = PetMatchCheck.objects.create(petmatch=pm)
		loggedin = client.login(username=user1.username, password=pwd1)
		response = client.post(URL_VERIFY_PETMATCHCHECK + str(pmc.id) + "/", {"verify-choice":"1"}, follow=True)
		activities = Activity.objects.filter(userprofile=user1.userprofile, activity="ACTIVITY_PETMATCHCHECK_VERIFY_SUCCESS")
		self.assertTrue(len(activities) == 0)
		loggedin = client.login(username=user2.username, password=pwd2)
		response = client.post(URL_VERIFY_PETMATCHCHECK + str(pmc.id) + "/", {"verify-choice":"2"}, follow=True)
		activities = Activity.objects.filter(userprofile=user1.userprofile, activity="ACTIVITY_PETMATCHCHECK_VERIFY_FAIL")
		self.assertTrue(len(activities) == 1)


class HomePageTesting (TestCase):
	def setUp(self):
		delete_all(leave_Users=False)
	def tearDown(self):
		delete_all(leave_Users=False)

	def test_get_petreports_json(self):
		results = setup_objects(num_users=5, create_petreports=True, num_petreports=10)
		user, pwd = random.choice(results["users"])
		client = random.choice(results["clients"])
		response = client.get(URL_HOME)
		self.assertEquals(response.status_code, 200)
		response = client.get(URL_GET_PETREPORTS_JSON, {"page":0}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request ["PATH_INFO"], URL_GET_PETREPORTS_JSON)

	def test_get_petmatches_json(self):
		results = setup_objects(num_users=5, create_petreports=True, num_petreports=10, create_petmatches=True, num_petmatches=5)
		user, pwd = random.choice(results["users"])
		client = random.choice(results["clients"])
		response = client.get(URL_HOME)
		self.assertEquals(response.status_code, 200)
		response = client.get(URL_GET_PETMATCHES_JSON, {"page":0}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request ["PATH_INFO"], URL_GET_PETMATCHES_JSON)

	def test_get_bookmarks_json(self):
		results = setup_objects(num_users=5, create_petreports=True, num_petreports=10, create_petmatches=True, num_petmatches=5)
		user, pwd = random.choice(results["users"])
		client = random.choice(results["clients"])
		client.login(username=user.username, password=pwd)
		response = client.get(URL_HOME)
		self.assertEquals(response.status_code, 200)
		response = client.get(URL_GET_BOOKMARKS_JSON, {"page":0}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_GET_BOOKMARKS_JSON)

	def test_get_petreunions_json(self):
		results = setup_objects(num_users=5, create_petreports=True, num_petreports=10, create_petmatches=True, num_petmatches=5, create_petreunions=True, num_petreunions=5)
		user, pwd = random.choice(results["users"])
		client = random.choice(results["clients"])
		response = client.get(URL_HOME)
		self.assertEquals(response.status_code, 200)
		response = client.get(URL_GET_PETREUNIONS_JSON, {"page":0}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_GET_PETREUNIONS_JSON)

	def test_get_activities_json(self):
		results = setup_objects(num_users=5, create_following_lists=True, create_petreports=True, num_petreports=10, create_petmatches=True, num_petmatches=5, create_petreunions=True, num_petreunions=5)
		user, pwd = random.choice(results["users"])
		client = random.choice(results["clients"])
		response = client.get(URL_HOME)
		self.assertEquals(response.status_code, 200)
		response = client.get(URL_GET_ACTIVITIES_JSON, {"page":0}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_GET_ACTIVITIES_JSON)

	def test_filter_petreports_pet_name(self):
		results = setup_objects(num_users=5, create_petreports=True, num_petreports=50)
		client = Client(enforce_csrf_checks=False)
		params = {"pet_name":"unknown", "page":0}
		response = client.get(URL_GET_PETREPORTS_JSON, params, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
		json_ids = [pr["ID"] for pr in json.loads(response._container[0])["pet_reports_list"]]
		params.pop("page")
		prs = PetReport.objects.filter(closed=False).filter(**params).order_by("id").reverse()
		for pr in prs:
			self.assertTrue(pr.pet_name == "unknown")
		pr_ids = [pr.id for pr in get_objects_by_page(prs, 1, limit=NUM_PETREPORTS_HOMEPAGE)]
		self.assertEquals(json_ids, pr_ids)

	def test_filter_petreports_status(self):
		results = setup_objects(num_users=5, create_petreports=True, num_petreports=50)
		client = Client(enforce_csrf_checks=False)
		params = {"status":"Lost", "page":0}
		response = client.get(URL_GET_PETREPORTS_JSON, params, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
		json_ids = [pr["ID"] for pr in json.loads(response._container[0])["pet_reports_list"]]
		params.pop("page")
		prs = PetReport.objects.filter(closed=False).filter(**params).order_by("id").reverse()
		for pr in prs:
			self.assertTrue(pr.status == "Lost")
		pr_ids = [pr.id for pr in get_objects_by_page(prs, 1, limit=NUM_PETREPORTS_HOMEPAGE)]
		self.assertEquals(json_ids, pr_ids)

	def test_filter_petreports_event_tag(self):
		results = setup_objects(num_users=5, create_petreports=True, num_petreports=50)
		client = Client(enforce_csrf_checks=False)
		params = {"event_tag":"Valley Fires", "page":0}
		response = client.get(URL_GET_PETREPORTS_JSON, params, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
		json_ids = [pr["ID"] for pr in json.loads(response._container[0])["pet_reports_list"]]
		params.pop("page")
		prs = PetReport.objects.filter(closed=False).filter(**params).order_by("id").reverse()
		for pr in prs:
			self.assertTrue(pr.event_tag == "Valley Fires")
		pr_ids = [pr.id for pr in get_objects_by_page(prs, 1, limit=NUM_PETREPORTS_HOMEPAGE)]
		self.assertEquals(json_ids, pr_ids)

	def test_filter_petreports_pet_type(self):
		results = setup_objects(num_users=5, create_petreports=True, num_petreports=50)
		client = Client(enforce_csrf_checks=False)
		params = {"pet_type":"Dog", "page":0}
		response = client.get(URL_GET_PETREPORTS_JSON, params, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
		json_ids = [pr["ID"] for pr in json.loads(response._container[0])["pet_reports_list"]]
		params.pop("page")
		prs = PetReport.objects.filter(closed=False).filter(**params).order_by("id").reverse()
		for pr in prs:
			self.assertTrue(pr.pet_type == "Dog")
		pr_ids = [pr.id for pr in get_objects_by_page(prs, 1, limit=NUM_PETREPORTS_HOMEPAGE)]
		self.assertEquals(json_ids, pr_ids)

	def test_filter_petreports_breed(self):
		results = setup_objects(num_users=5, create_petreports=True, num_petreports=50)
		client = Client(enforce_csrf_checks=False)
		params = {"pet_type":"Dog", "breed":"Laborador Retriever", "page":0}
		response = client.get(URL_GET_PETREPORTS_JSON, params, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
		json_ids = [pr["ID"] for pr in json.loads(response._container[0])["pet_reports_list"]]
		params.pop("page")
		prs = PetReport.objects.filter(closed=False).filter(**params).order_by("id").reverse()
		for pr in prs:
			self.assertTrue(pr.pet_type == "Dog" and pr.breed == "Laborador Retriever")
		pr_ids = [pr.id for pr in get_objects_by_page(prs, 1, limit=NUM_PETREPORTS_HOMEPAGE)]
		self.assertEquals(json_ids, pr_ids)

	def test_filter_petreports_breed_all(self):
		results = setup_objects(num_users=5, create_petreports=True, num_petreports=50)
		client = Client(enforce_csrf_checks=False)
		params = {"pet_type":"Dog", "breed":"All", "page":1}
		response = client.get(URL_GET_PETREPORTS_JSON, params, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
		json_ids = [pr["ID"] for pr in json.loads(response._container[0])["pet_reports_list"]] #Returns nothing
		params.pop("page")
		prs = PetReport.objects.filter(closed=False).filter(**params).order_by("id").reverse() #Also Returns nothing
		for pr in prs:
			self.assertTrue(pr.pet_type == "Dog")
		pr_ids = [pr.id for pr in get_objects_by_page(prs, 1, limit=NUM_PETREPORTS_HOMEPAGE)]
		self.assertEquals(json_ids, pr_ids)

		#Now try replicating the "All" with the absence of it.
		params = {"pet_type":"Dog", "page":1}
		response = client.get(URL_GET_PETREPORTS_JSON, params, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
		json_ids = [pr["ID"] for pr in json.loads(response._container[0])["pet_reports_list"]] #Returns nothing
		params.pop("page")
		prs = PetReport.objects.filter(closed=False).filter(**params).order_by("id").reverse() #Also Returns nothing
		for pr in prs:
			self.assertTrue(pr.pet_type == "Dog")
		pr_ids = [pr.id for pr in get_objects_by_page(prs, 1, limit=NUM_PETREPORTS_HOMEPAGE)]
		self.assertEquals(json_ids, pr_ids)



class RegistrationTesting (TestCase):
	def setUp(self):
		delete_all(leave_Users=False)
	def tearDown(self):
		delete_all(leave_Users=False)

	def test_good_register(self):
		client = Client(enforce_csrf_checks=False)
		post = {
			"username":generate_string(10),
			"email": generate_string(6) + "@test.com",
			"tos": "true",
			"first_name": generate_string(10),
			"last_name": generate_string(15),
			"guardian_email": generate_string(6) + "@testguardian.com",
			"password1": "password",
			"password2": "password",
			"date_of_birth": generate_random_birthdate()
		}
		response = client.post(URL_REGISTRATION, post, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request ["PATH_INFO"], URL_HOME)

	def test_bad_register (self):
		client = Client(enforce_csrf_checks=False)
		response = client.get(URL_LOGIN)
		self.assertEquals(response.status_code, 200)
		response = client.get(URL_REGISTRATION)
		self.assertEquals(response.status_code, 200)
		username = generate_string(10)
		first_name = generate_string(10)
		last_name = generate_string(15)
		email = generate_string(6) + "@test.com"
		guardian_email = generate_string(6) + "@testguardian.com"
		password = generate_string (10)
		date_of_birth = generate_random_birthdate()
		#Test duplicate email
		User.objects.create_user(username=generate_string(10) + "a", email=email, password=password)
		post = {
			"username":username,
			"email":email,
			"tos": "true",
			"first_name": first_name,
			"last_name": last_name,
			"guardian_email":guardian_email,
			"password1":password,
			"password2":password,
			"date_of_birth":date_of_birth
		}

		response = client.post(URL_REGISTRATION, post, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request ["PATH_INFO"], URL_REGISTRATION)
		#Test duplicate username
		User.objects.create_user(username=username, email=email, password=password)
		post["email"] = "someotheremail@test.com"
		response = client.post(URL_REGISTRATION, post, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request ["PATH_INFO"], URL_REGISTRATION)
		#Test inconsistent passwords.
		post["username"] = "someotherusername"
		post["password2"] = "different_password"
		response = client.post(URL_REGISTRATION, post, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request ["PATH_INFO"], URL_REGISTRATION)
