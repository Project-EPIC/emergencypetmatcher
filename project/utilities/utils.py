from PIL import Image
from random import randint
from datetime import datetime
from django.core.validators import validate_email
from reporting.constants import *
from django.conf import settings
import os, re, hashlib, random, string, sys, time, lipsum, traceback

'''===================================================================================
utils.py: Utility Functions for EPM Utility and Testing

When writing your test file (tests.py), make sure to have the following import:

	from utilities.utils import *
==================================================================================='''

#Setup Lorem Ipsum Generator}
LIPSUM = lipsum.Generator()
LIPSUM.sentence_mean = 4
LIPSUM.sentence_sigma = 1
LIPSUM.paragraph_mean = 3
LIPSUM.paragraph_sigma = 1

#SHA1 Compiler.
SHA1_RE = re.compile('^[a-f0-9]{40}$')

def print_testing_name(test_name, single_test=False):
	if single_test == True:
		print "\n[TEST]: Testing {%s}\n" % (test_name)
	else:
		print "\n[TEST]: Testing {%s} for %s iterations\n" % (test_name, NUMBER_OF_TESTS)

def print_info_msg (string):
	print "[INFO]: %s" % string
def print_test_msg (string):
	print "[TEST]: %s" % string	
def print_debug_msg (string):
	print "[DEBUG]: %s" % string	
def print_success_msg (string):
	print "[OK]: %s" % string	
def print_error_msg (string):
	print "[ERROR]: %s" % string

def email_is_valid(email_address):
	try:
		if validate_email(email_address) == None:
			return True
	except:
		return False
		
def get_objects_by_page(objects, page, limit=25):
    if (page != None and page > 0):
        page = int(page)
        objects = objects[((page-1) * limit):((page-1) * limit + limit)]
    return objects 

# This function generates two dictionaries: the first representing the original contact for this petreport
# and the second the cross-posting contact. Both are contingent upon whether contact fields have been
# prepared for this petreport.
def generate_pet_contacts(petreport):
	userprofile_contact = {	"name": petreport.proposed_by.user.username, 
							"email": petreport.proposed_by.user.email, 
							"phone": None, 
							"link": None }

	if petreport.is_crossposted() == True:
		return({"name": petreport.contact_name, 
				"email": petreport.contact_email, 
				"phone": petreport.contact_number, 
				"link": petreport.contact_link }, userprofile_contact)
	else:
		return (userprofile_contact, None)		

def create_sha1_hash(username):
	salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
	if isinstance(username, unicode):
		username = username.encode("utf-8")
	return hashlib.sha1(salt + username).hexdigest()

#Generate a random alpha-numeric string.
def generate_string (size, phone=False, url=False, chars = string.ascii_uppercase + string.digits):
	if phone == True:
		number = "(" + str(randint(10**(3-1), (10**3)-1)) + ")-"
		number = number + str(randint(10**(3-1), (10**3)-1)) + "-"
		number = number + str(randint(10**(4-1), (10**4)-1))
		return number

	elif url == True:
		return "http://" + ''.join(random.choice(chars) for i in range(size))

	else: 
		return ''.join(random.choice(chars) for i in range(size))

def generate_lipsum_paragraph(max_length):
	result =  LIPSUM.generate_paragraph()
	#Make sure that the length does not exceed max_length...
	if len(result) > max_length:
		return generate_lipsum_paragraph(max_length)
	else:
		return result

#Keep the user/tester updated.
def output_update (i, iterations=NUMBER_OF_TESTS):	
	output = "%d of %d iterations complete\n\n" % (i, iterations)
	sys.stdout.write("\r\x1b[K"+output.__str__())
	sys.stdout.flush()

#Given an image path, create an Image and return it, catching and ignoring any errors.
def open_image(img_path):
	try:
		img = None
		img = Image.open(img_path)
		img.load()
	except IOError:
		pass
	return img


def generate_random_birthdate():
	year = random.choice(range(1950, 2005))
	month = random.choice(range(1, 12))
	day = random.choice(range(1, 28))
	birthDate = datetime(year, month, day).strftime("%m/%d/%Y")
	return birthDate

#Given Date of Birth (DOB), return True if User with Input DOB is a minor, false otherwise.
def is_minor(date_of_birth):
	now = datetime.now()
	dob = datetime.strptime(date_of_birth, "%m/%d/%Y")
	age = (now - dob).days / 365.25
	if age < 18:
		return True
	return False

#generate_random_date(): Referenced from: http://stackoverflow.com/questions/553303/generate-a-random-date-between-two-other-dates
def generate_random_date(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(format, time.localtime(ptime))

#Give the lap time (and AVG) for a 'critical section'.
def performance_report(total_time):
	print '\tTotal Time: %s sec' % (total_time)
	print '\tAVG Time Taken for a Single Test: %s sec\n' % (total_time/NUMBER_OF_TESTS)

#Place sample petreport image lists in memory. Used for generating random PetReports with sample images.
def load_PetReport_sample_images():
	for img in os.listdir(PETREPORT_SAMPLES_DOG_DIRECTORY):
		if img != ".DS_Store" and img != ".anchor":
			PETREPORT_SAMPLE_DOG_IMAGES.append("petreport/samples/dog/" + img)
	for img in os.listdir(PETREPORT_SAMPLES_CAT_DIRECTORY):
		if img != ".DS_Store" and img != ".anchor":
			PETREPORT_SAMPLE_CAT_IMAGES.append("petreport/samples/cat/" + img)
	for img in os.listdir(PETREPORT_SAMPLES_BIRD_DIRECTORY):
		if img != ".DS_Store" and img != ".anchor":
			PETREPORT_SAMPLE_BIRD_IMAGES.append("petreport/samples/bird/" + img)
	for img in os.listdir(PETREPORT_SAMPLES_HORSE_DIRECTORY):
		if img != ".DS_Store" and img != ".anchor":
			PETREPORT_SAMPLE_HORSE_IMAGES.append("petreport/samples/horse/" + img)
	for img in os.listdir(PETREPORT_SAMPLES_RABBIT_DIRECTORY):
		if img != ".DS_Store" and img != ".anchor":
			PETREPORT_SAMPLE_RABBIT_IMAGES.append("petreport/samples/rabbit/" + img)
	for img in os.listdir(PETREPORT_SAMPLES_SNAKE_DIRECTORY):
		if img != ".DS_Store" and img != ".anchor":
			PETREPORT_SAMPLE_SNAKE_IMAGES.append("petreport/samples/snake/" + img)
	for img in os.listdir(PETREPORT_SAMPLES_TURTLE_DIRECTORY):
		if img != ".DS_Store" and img != ".anchor":
			PETREPORT_SAMPLE_TURTLE_IMAGES.append("petreport/samples/turtle/" + img)








