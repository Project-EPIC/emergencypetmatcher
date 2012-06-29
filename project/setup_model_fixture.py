"""
setup_model_fixture.py: Create sample data for all models.
"""
from home.models import *
from django.contrib.auth import authenticate
import string, random, sys, os

'''Control Variables'''
NUM_PETREPORTS = 100
NUM_USERS = 5

def generate_string (size, chars = string.ascii_uppercase + string.digits):
		return ''.join(random.choice(chars) for i in range(size))

#Get rid of all objects in the QuerySet.
def delete_all():
	User.objects.all().delete()
	UserProfile.objects.all().delete()
	PetMatch.objects.all().delete()
	PetReport.objects.all().delete()
	Chat.objects.all().delete()
	ChatLine.objects.all().delete()

'''''''''''''''''''''''''''''''''''''''''''''''''''
Create a UserProfile object
'''''''''''''''''''''''''''''''''''''''''''''''''''
def create_user():
	username = generate_string(10)
	password = generate_string(10)
	email = generate_string(6) + '@' + 'test.com'
	user = User.objects.create_user(username = username, email = email, password = password)
	return (user, password)

'''''''''''''''''''''''''''''''''''''''''''''''''''
Create Objects for: PetReport
'''''''''''''''''''''''''''''''''''''''''''''''''''
def create_petreport(user):
	pet_type = random.choice(PET_TYPE_CHOICES[1:])[0]
	status = u'%s' % random.choice(STATUS_CHOICES [1:])[0]
	pr = PetReport (pet_type = pet_type, status = status, proposed_by = user.get_profile())
	pr.pet_name = generate_string(30)
	pr.description = generate_string(300)
	pr.sex = random.choice(SEX_CHOICES[1:])[0]
	pr.location = generate_string(50)
	pr.color = generate_string(20)
	pr.breed = generate_string(30)
	pr.size = generate_string(30)
	pr.age = random.randrange(0,15)
	pr.save() 

'''''''''''''''''''''''''''''''''''''''''''''''''''
When Executed: Setup our fixture
'''''''''''''''''''''''''''''''''''''''''''''''''''

print '\nSetting up model fixture....'
delete_all()
users = []
passwords = []
for i in range (NUM_USERS):
	user, pwd = create_user()
	users.append(user)
	passwords.append(pwd)

for i in range (NUM_PETREPORTS):
	create_petreport(random.choice(users))

print '%d users created, %s pet reports created' % (NUM_USERS, NUM_PETREPORTS)
print 'usernames with passwords are:'
for i in range (NUM_USERS):
	print '<%s, %s>' % (users[i].username, passwords[i])