from django.contrib.auth import authenticate
from django.test.client import Client
from django.test import TestCase
from django.forms.models import model_to_dict
from utilities.utils import *
from fixture import *
from pprint import pprint
from django.contrib.messages import constants as messages
import unittest, string, random, sys, time, ipdb

class PetMatchTesting(TestCase):
	def setUp(self):
		delete_all(leave_Users=False)
	def tearDown(self):
		delete_all(leave_Users=False)

	def test_save_petmatch(self):
		user, password = create_random_User()
		user2, password2 = create_random_User()
		user3, password3 = create_random_User()
		pet_type = random.choice(PET_TYPE_CHOICES)[0]
		pr1 = create_random_PetReport(user2, status = "Lost", pet_type = pet_type)
		pr2 = create_random_PetReport(user3, status = "Found", pet_type = pet_type)
		pm = create_random_PetMatch(pr1, pr2, user, pet_type=pet_type)
		pm_same = PetMatch.objects.get(proposed_by = user.userprofile)
		self.assertEqual(pm.lost_pet, pm_same.lost_pet)
		self.assertEqual(pm.found_pet, pm_same.found_pet)
		self.assertEqual(pm.proposed_by, pm_same.proposed_by)
		self.assertEqual(pm, pm_same)

	def test_save_improperly_saved_petmatch(self):
		user, password = create_random_User()
		user2, password2 = create_random_User()
		user3, password3 = create_random_User()
		pet_type = random.choice(PET_TYPE_CHOICES)[0]
		pr_lost = create_random_PetReport(status="Lost")
		pr_found = create_random_PetReport(status="Found")
		pm = create_random_PetMatch(lost_pet=pr_found, found_pet=pr_lost)
		self.assertEquals(pm, None)
		self.assertEquals(PetMatch.objects.filter(lost_pet=pr_found, found_pet=pr_lost).exists(), False)

	def test_save_duplicate_petmatch(self):
		u1 = create_random_User()
		u2 = create_random_User()
		pet_type = random.choice(PET_TYPE_CHOICES)[0]
		pr_lost = create_random_PetReport(status="Lost")
		pr_found = create_random_PetReport(status="Found")
		pm = create_random_PetMatch(lost_pet=pr_lost, found_pet=pr_found, user = u1[0])
		pm_duplicate = create_random_PetMatch(lost_pet=pr_lost, found_pet=pr_found, user = u2[0])
		self.assertFalse(pm == None)
		self.assertEquals(pm_duplicate, None)
		self.assertEquals(PetMatch.objects.filter(lost_pet=pr_lost, found_pet=pr_found, proposed_by__user = u1[0]).exists(), True)
		self.assertEquals(PetMatch.objects.filter(lost_pet=pr_lost, found_pet=pr_found, proposed_by__user = u2[0]).exists(), False)

	def test_update_petmatch(self):
		user, password = create_random_User()
		user2, password2 = create_random_User()
		user3, password3 = create_random_User()
		pet_type = random.choice(PET_TYPE_CHOICES)[0]
		pr1 = create_random_PetReport(user2, status = "Lost", pet_type = pet_type)
		pr2 = create_random_PetReport(user3, status = "Found", pet_type = pet_type)
		pm = create_random_PetMatch(pr1, pr2, user, pet_type=pet_type)

		pm.down_votes = create_random_Userlist()
		pm.up_votes = create_random_Userlist()
		pm.save()
		pm_updated = PetMatch.objects.get(proposed_by=user.userprofile, lost_pet=pr1, found_pet=pr2)
		self.assertEqual(pm, pm_updated)
		self.assertEqual(len(pm.down_votes.all()), len(pm_updated.down_votes.all()))
		self.assertEqual(len(pm.up_votes.all()), len(pm_updated.up_votes.all()))
		self.assertEqual(pm.is_successful(), pm_updated.is_successful())

	def test_delete_petmatch(self):
		user, password = create_random_User()
		user2, password2 = create_random_User()
		user3, password3 = create_random_User()
		pet_type = random.choice(PET_TYPE_CHOICES)[0]
		pr1 = create_random_PetReport(user2, status = "Lost", pet_type = pet_type)
		pr2 = create_random_PetReport(user3, status = "Found", pet_type = pet_type)
		pm = create_random_PetMatch(pr1, pr2, user, pet_type=pet_type)
		PetMatch.objects.all().get(proposed_by = user.userprofile, lost_pet = pr1, found_pet = pr2).delete()
		self.assertTrue(len(PetMatch.objects.all()) == 0)

class MatchingTesting (TestCase):
	def setUp(self):
		delete_all(leave_Users=False)
	def tearDown(self):
		delete_all(leave_Users=False)

	def test_get_ordered_candidate_petreports(self):
		user, pwd = create_random_User()
		user2, pwd2 = create_random_User()
		pet_type = random.choice(PET_TYPE_CHOICES)[0]
		pr1 = create_random_PetReport(user, status="Lost", pet_type=pet_type)
		pr2 = create_random_PetReport(user2, status="Found", pet_type=pet_type)
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username = user.username, password=pwd)

		for i in range(50):
			create_random_PetReport(pet_type=pet_type)

		response = client.get(URL_GET_CANDIDATE_PETREPORTS_JSON, {"target_petreport_id": pr1.id, "page":1}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		json_ids = [pr["ID"] for pr in json.loads(response._container[0])["pet_reports_list"]]
		candidates = pr1.get_ranked_candidate_PetReports(pr1.get_candidate_PetReports(), page=1)

		for i in range(len(candidates)):
			self.assertEquals(candidates[i].id, json_ids[i])

	def test_get_matching_interface_success(self):
		user, pwd = create_random_User()
		user2, pwd2 = create_random_User()
		pet_type = random.choice(PET_TYPE_CHOICES)[0]
		pr1 = create_random_PetReport(user, status="Lost", pet_type=pet_type)
		pr2 = create_random_PetReport(user2, status="Found", pet_type=pet_type)
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username = user.username, password=pwd)
		response = client.get(URL_MATCHING + str(pr1.id))
		self.assertEquals(response.status_code, 200)

	def test_get_matching_interface_fail(self):
		user, pwd = create_random_User()
		user2, pwd2 = create_random_User()
		pet_type = random.choice(PET_TYPE_CHOICES)[0]
		pr1 = create_random_PetReport(user, status="Lost", pet_type=pet_type)
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username = user.username, password=pwd)
		response = client.get(URL_MATCHING + str(pr1.id))
		self.assertEquals(response.status_code, 200)
		self.assertTrue(response.request["PATH_INFO"], URL_HOME)

	def test_get_propose_petmatch_success (self):
		user, pwd = create_random_User()
		user2, pwd2 = create_random_User()
		pet_type = random.choice(PET_TYPE_CHOICES)[0]
		pr1 = create_random_PetReport(user, status="Lost", pet_type=pet_type)
		candidate = create_random_PetReport(user, status="Found", pet_type=pet_type)
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username = user.username, password=pwd)
		response = client.get(URL_MATCHING + "%d" % (pr1.id))
		response = client.post(URL_MATCHING + "%d" % (pr1.id), {"candidate_id":candidate.id})
		response = client.get(URL_PROPOSE_PETMATCH + "%d/%d/" % (pr1.id, candidate.id))
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_PROPOSE_PETMATCH + "%d/%d/" % (pr1.id, candidate.id))

	def test_get_propose_petmatch_fail (self):
		user, pwd = create_random_User()
		user2, pwd2 = create_random_User()
		pr1 = create_random_PetReport(user, status="Lost", pet_type="Dog")
		candidate = create_random_PetReport(user, status="Lost", pet_type="Dog")
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username = user.username, password=pwd)
		response = client.get(URL_PROPOSE_PETMATCH + "%d/%d/" % (pr1.id, candidate.id), follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertTrue(response.request["PATH_INFO"] != URL_PROPOSE_PETMATCH + "%d/%d/" % (pr1.id, candidate.id))
		candidate = create_random_PetReport(user, status="Found", pet_type="Cat")
		response = client.get(URL_PROPOSE_PETMATCH + "%d/%d/" % (pr1.id, candidate.id), follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertTrue(response.request["PATH_INFO"] != URL_PROPOSE_PETMATCH + "%d/%d/" % (pr1.id, candidate.id))

	def test_propose_petmatch_success(self):
		user, pwd = create_random_User()
		user2, pwd2 = create_random_User()
		pr1 = create_random_PetReport(user, status="Lost", pet_type="Dog")
		candidate = create_random_PetReport(user, status="Found", pet_type="Dog")
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username = user.username, password=pwd)
		settings.RECAPTCHA_SERVER_SECRET=settings.TEST_RECAPTCHA_SERVER_SECRET
		response = client.get(URL_MATCHING + "%d" % (pr1.id))
		response = client.post(URL_MATCHING + "%d" % (pr1.id), {"candidate_id":candidate.id})
		response = client.get(URL_PROPOSE_PETMATCH + "%d/%d/" % (pr1.id, candidate.id))
		response = client.post(URL_PROPOSE_PETMATCH + "%d/%d/" % (pr1.id, candidate.id), {"g-recaptcha-response":settings.TEST_RECAPTCHA_CLIENT_SECRET}, follow=True)
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_HOME)

	def test_get_petmatch_page(self):
		user, pwd = create_random_User()
		user2, pwd2 = create_random_User()
		pr1 = create_random_PetReport(user, status="Lost", pet_type="Dog")
		candidate = create_random_PetReport(user, status="Found", pet_type="Dog")
		pm = create_random_PetMatch(user=user, lost_pet=pr1, found_pet=candidate)
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username = user.username, password=pwd)
		response = client.get(URL_PMDP + "%d/" % (pm.id))
		self.assertEquals(response.status_code, 200)
		self.assertEquals(response.request["PATH_INFO"], URL_PMDP + "%d/" % (pm.id))

	def test_upvote_petmatch(self):
		results = setup_objects(create_users=True, num_users=10)
		user, pwd = results["users"][0]
		user2, pwd2 = results["users"][1]
		pr1 = create_random_PetReport(user, status="Lost", pet_type="Dog")
		pr2 = create_random_PetReport(user2, status="Found", pet_type="Dog")
		pm = PetMatch.objects.create(proposed_by=user.userprofile, lost_pet=pr1, found_pet=pr2)
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username = user.username, password=pwd)
		response = client.post(URL_VOTE_PETMATCH + str(pm.id), {"vote":"upvote"}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
		self.assertEquals(response.status_code, 200)
		pm = PetMatch.objects.get()
		self.assertEquals(pm.up_votes.count(), 1)
		self.assertEquals(pm.down_votes.count(), 0)

	def test_downvote_petmatch(self):
		results = setup_objects(create_users=True, num_users=10)
		user, pwd = results["users"][0]
		user2, pwd2 = results["users"][1]
		pr1 = create_random_PetReport(user, status="Lost", pet_type="Dog")
		pr2 = create_random_PetReport(user2, status="Found", pet_type="Dog")
		pm = PetMatch.objects.create(proposed_by=user.userprofile, lost_pet=pr1, found_pet=pr2)
		client = Client(enforce_csrf_checks=False)
		loggedin = client.login(username = user.username, password=pwd)
		response = client.post(URL_VOTE_PETMATCH + str(pm.id), {"vote":"downvote"}, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
		self.assertEquals(response.status_code, 200)
		pm = PetMatch.objects.get()
		self.assertEquals(pm.down_votes.count(), 1)
		self.assertEquals(pm.up_votes.count(), 0)
