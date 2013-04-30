import os

'''===================================================================================
[constants.py]: Constants for the EPM system
==================================================================================='''

#Number of Tests
NUMBER_OF_TESTS = 20

#Lower and Upper bounds for Lost and Found Dates
DATE_LOWER_BOUND = "2012-01-01"
DATE_UPPER_BOUND = "2012-08-16"

#number of pet reports on the home page
NUM_PETREPORTS_HOMEPAGE = 50

#max_length for Model Fields
USER_USERNAME_LENGTH = 30
USER_FIRSTNAME_LENGTH = 30
USER_LASTNAME_LENGTH = 30
USER_PASSWORD_LENGTH = 30
PETREPORT_PET_TYPE_LENGTH = 10
PETREPORT_STATUS_LENGTH = 5
PETREPORT_SEX_LENGTH = 6
PETREPORT_SIZE_LENGTH = 30
PETREPORT_LOCATION_LENGTH = 100
PETREPORT_PET_NAME_LENGTH = 15 
PETREPORT_MICROCHIP_ID_LENGTH = 40
PETREPORT_TAG_INFO_LENGTH = 1000
PETREPORT_CONTACT_NAME_LENGTH = 20
PETREPORT_CONTACT_NUMBER_LENGTH = 15
PETREPORT_CONTACT_EMAIL_LENGTH = 30
PETREPORT_AGE_LENGTH = 10
PETREPORT_COLOR_LENGTH =30
PETREPORT_BREED_LENGTH = 30
PETREPORT_DESCRIPTION_LENGTH = 1000
PETREPORT_SPAYED_OR_NEUTERED_LENGTH = 10
PETMATCH_DESCRIPTION_LENGTH = 300
PETMATCH_VERIFICATION_VOTES_LENGTH = 2
CHATLINE_TEXT_LENGTH = 10000

#Small List of Names
USERNAMES = ['Jacob', 'Emily', 'Joshua', 'Madison', 'Kenneth', 'Mark', 'Dave', 'Angela', '' 'Matthew', 'Olivia', 'Daniel', 'Hannah', 
'Chris', 'Abby', 'Andrew', 'Isabella', 'Mario', 'Sahar', 'Amrutha', 'Leysia', 'Ken', 'Abe']
PETREPORT_NAMES = ['Sparky', 'Nugget', 'Sydney', 'Missy', 'Marley', 'Fousey', 'Daisy', 'Libby', 'Apollo', 'Bentley', 'Scruffy',
'Dandy', 'Candy', 'Mark', 'Baby', 'Toodle', 'Princess' ,'Prince', 'Guss']

#Identifiers
UPVOTE = "upvote"
DOWNVOTE = "downvote"
PETREPORT_PET_TYPE_DOG = "Dog"
PETREPORT_PET_TYPE_CAT = "Cat"
PETREPORT_PET_TYPE_BIRD = "Bird"
PETREPORT_PET_TYPE_HORSE = "Horse"
PETREPORT_PET_TYPE_RABBIT = "Rabbit"
PETREPORT_PET_TYPE_SNAKE = "Snake"
PETREPORT_PET_TYPE_TURTLE = "Turtle"
PETREPORT_PET_TYPE_OTHER = "Other"

#PetMatch Constants
PETMATCH_OUTCOME_NEW_PETMATCH = "NEW PETMATCH"
PETMATCH_OUTCOME_DUPLICATE_PETMATCH = "DUPCLIATE PETMATCH"
PETMATCH_OUTCOME_UPDATE = "SQL UPDATE"
PETMATCH_OUTCOME_INSERTED_IMPROPERLY = "INSERTED IMPROPERLY"

#File Path Constants
ACTIVITY_LOG_DIRECTORY = os.path.dirname(os.path.dirname(__file__)) + "/logs/activity_logs/"
TEST_ACTIVITY_LOG_DIRECTORY = os.path.dirname(os.path.dirname(__file__)) + "/logs/test_activity_logs/"
PETREPORT_IMAGES_DIRECTORY = os.path.dirname(os.path.dirname(__file__)) + "/static/images/petreport_images/"
PETREPORT_SAMPLE_IMAGES_DIRECTORY = os.path.dirname(os.path.dirname(__file__)) + "/static/images/petreport_sample_images/"
PETREPORT_SAMPLE_DOG_IMAGES_DIRECTORY = PETREPORT_SAMPLE_IMAGES_DIRECTORY + "dog/"
PETREPORT_SAMPLE_CAT_IMAGES_DIRECTORY = PETREPORT_SAMPLE_IMAGES_DIRECTORY + "cat/"
PETREPORT_SAMPLE_BIRD_IMAGES_DIRECTORY = PETREPORT_SAMPLE_IMAGES_DIRECTORY + "bird/"
PETREPORT_SAMPLE_HORSE_IMAGES_DIRECTORY = PETREPORT_SAMPLE_IMAGES_DIRECTORY + "horse/"
PETREPORT_SAMPLE_RABBIT_IMAGES_DIRECTORY = PETREPORT_SAMPLE_IMAGES_DIRECTORY + "rabbit/"
PETREPORT_SAMPLE_SNAKE_IMAGES_DIRECTORY = PETREPORT_SAMPLE_IMAGES_DIRECTORY + "snake/"
PETREPORT_SAMPLE_TURTLE_IMAGES_DIRECTORY = PETREPORT_SAMPLE_IMAGES_DIRECTORY + "turtle/"
USERPROFILE_IMAGES_DIRECTORY = os.path.dirname(os.path.dirname(__file__)) + "/static/images/profile_images/"

#List of sample PetReport Dog images
PETREPORT_SAMPLE_DOG_IMAGES = []
#List of sample PetReport Cat images
PETREPORT_SAMPLE_CAT_IMAGES = []
#List of sample PetReport Bird images
PETREPORT_SAMPLE_BIRD_IMAGES = []
#List of sample PetReport Horse images
PETREPORT_SAMPLE_HORSE_IMAGES = []
#List of sample PetReport Rabbit images
PETREPORT_SAMPLE_RABBIT_IMAGES = []
#List of sample PetReport Snake images
PETREPORT_SAMPLE_SNAKE_IMAGES = []
#List of sample PetReport Turtle images
PETREPORT_SAMPLE_TURTLE_IMAGES = []

#Activity Enum Values
ACTIVITY_ACCOUNT_CREATED = "ACCOUNT_CREATED"
ACTIVITY_LOGIN = "LOGIN"
ACTIVITY_LOGOUT = "LOGOUT"
ACTIVITY_PETREPORT_SUBMITTED = "PETREPORT_SUBMITTED"
ACTIVITY_PETREPORT_ADD_BOOKMARK = "PETREPORT_ADD_BOOKMARK"
ACTIVITY_PETREPORT_REMOVE_BOOKMARK = "PETREPORT_REMOVE_BOOKMARK"
ACTIVITY_PETMATCH_PROPOSED = "PETMATCH_PROPOSED"
ACTIVITY_PETMATCH_UPVOTE = "PETMATCH_UPVOTE"
ACTIVITY_PETMATCH_UPVOTE_SUCCESSFUL = "PETMATCH_UPVOTE_SUCCESSFUL"
ACTIVITY_PETMATCH_DOWNVOTE= "PETMATCH_DOWNVOTE"
ACTIVITY_FOLLOWING = "_FOLLOWING"
ACTIVITY_UNFOLLOWING = "UNFOLLOWING"
ACTIVITY_FOLLOWER = "_FOLLOWER"
ACTIVITY_UNFOLLOWER = "UNFOLLOWER"
ACTIVITY_PETMATCH_PROPOSED_LOST_BOOKMARKED_PETREPORT = "PETMATCH_LOST_BOOKMARKED_PETREPORT"
ACTIVITY_PETMATCH_PROPOSED_FOUND_BOOKMARKED_PETREPORT = "PETMATCH_FOUND_BOOKMARKED_PETREPORT"
ACTIVITY_USER_CHANGED_USERNAME = "USER_CHANGED_USERNAME"
ACTIVITY_USER_BEING_FOLLOWED = "USER_BEING_FOLLOWED"
ACTIVITY_USER_BEING_UNFOLLOWED = "USER_BEING_UNFOLLOWED"
ACTIVITY_USER_PROPOSED_PETMATCH_UPVOTE = "USER_PROPOSED_PETMATCH_UPVOTE"
ACTIVITY_USER_PROPOSED_PETMATCH_SUCCESSFUL = "USER_PROPOSED_PETMATCH_SUCCESSFUL"
ACTIVITY_USER_PROPOSED_PETMATCH_FAILURE = "USER_PROPOSED_PETMATCH_FAILURE"
ACTIVITY_USER_VERIFY_PETMATCH_SUCCESSFUL = "USER_VERIFY_PETMATCH_SUCCESSFUL"
ACTIVITY_USER_SEND_MESSAGE_TO_USERPROFILE = "ACTIVITY_USER_SEND_MESSAGE_TO_USER "

#Reputation reward points
REWARD_PETMATCH_VOTE = 2
REWARD_PETMATCH_UPVOTE_SUCCESSFUL = 10
REWARD_PETMATCH_PROPOSE = 5
REWARD_PETREPORT_SUBMIT = 5
REWARD_PETREPORT_BOOKMARK = 1
REWARD_USER_FOLLOWED = 2
#Reward this user for his/her proposed petmatch being voted
REWARD_USER_PROPOSED_PETMATCH_VOTE = 5 
REWARD_USER_PROPOSED_PETMATCH_SUCCESSFUL = 25
REWARD_USER_PROPOSED_PETMATCH_FAILURE = 15
REWARD_USER_VERIFY_PETMATCH_SUCCESSFUL = 15
REWARD_NEW_ACCOUNT = 10


#Represents how many activities to fetch per request.
ACTIVITY_FEED_LENGTH = 10

#URLS - use for redirect calls
URL_HOME = '/'
URL_GET_ACTIVITIES = "/get_activities_json"
URL_LOGIN = '/login'
URL_SUBMIT_PETREPORT ='/reporting/submit_PetReport'
URL_USERPROFILE = '/UserProfile/'
URL_PRDP = '/reporting/PetReport/'
URL_PMDP = '/matching/PetMatch/'
URL_VOTE_MATCH = '/matching/vote_PetMatch'
URL_MATCHING = "/matching/match_PetReport/"
URL_PROPOSE_MATCH = "/matching/propose_PetMatch/"
URL_BOOKMARK_PETREPORT = "/reporting/bookmark_PetReport"
URL_BOOKMARKED = "/reporting/bookmarks/"
URL_FOLLOW = "/follow"
URL_UNFOLLOW = "/unfollow"
URL_EDITUSERPROFILE = "/edituserprofile"
URL_EMAIL_VERIFICATION_COMPLETE = "/email_verification_complete/" 
URL_VERIFY_PETMATCH = "/matching/verify_PetMatch/"
URL_SEND_MESSAGE_TO_USERPROFILE = "/UserProfile/message_UserProfile"


#HTML File Paths (relative to STATIC_URL) - use for render_to_response calls
HTML_HOME = "home/index.html"
HTML_LOGIN = "registration/login.html"
HTML_ABOUT = "home/about.html"
HTML_SUBMIT_PETREPORT = "reporting/petreport_form.html"
HTML_USERPROFILE = "home/userprofile.html"
HTML_PRDP = "reporting/petreport.html"
HTML_PMDP = "matching/petmatch.html"
HTML_MATCHING = "matching/matching.html"
HTML_PROPOSE_MATCH = "matching/propose_match.html"
HTML_SOCIAL_AUTH_FORM = "registration/social_auth_username_form.html"
HTML_VERIFY_PETMATCH = "matching/verify_petmatch.html"
HTML_SOCIAL_AUTH_FORM = "registration/social_auth_form.html"
HTML_EDITUSERPROFILE_FORM ="home/EditUserProfile_form.html"

TEXTFILE_EMAIL_ACTIVATION_SUBJECT="registration/activation_email_subject.txt"
TEXTFILE_EMAIL_CHANGE_VERICATION="home/email_change_verification.txt"
TEXTFILE_EMAIL_PETOWNER_VERIFY_PETMATCH = "matching/verification_email_to_pet_owner.txt"
TEXTFILE_EMAIL_PETMATCH_PROPOSER = "matching/verification_email_to_digital_volunteer.txt"
TEXTFILE_EMAIL_USERPROFILE_MESSAGE = "home/email_message_user.txt"

#E-mail Constants
EMAIL_SUBJECT_PETOWNER_VERIFY_PETMATCH="Emergency Pet Matcher: We have found a potential match for your pet!"
EMAIL_SUBJECT_PETMATCH_PROPOSER='EmergencyPetMatcher: Your pet match is close to being successful!'
TEST_EMAIL="emergencypetmatchertest@gmail.com"


#Place sample petreport image lists in memory as global variables. Used for generating random PetReports with sample images.
def load_PetReport_sample_images():
	for img in os.listdir(PETREPORT_SAMPLE_DOG_IMAGES_DIRECTORY):
		if img != ".DS_Store" and img != ".anchor":
			PETREPORT_SAMPLE_DOG_IMAGES.append("images/petreport_sample_images/dog/" + img)
	for img in os.listdir(PETREPORT_SAMPLE_CAT_IMAGES_DIRECTORY):
		if img != ".DS_Store" and img != ".anchor":
			PETREPORT_SAMPLE_CAT_IMAGES.append("images/petreport_sample_images/cat/" + img)
	for img in os.listdir(PETREPORT_SAMPLE_BIRD_IMAGES_DIRECTORY):
		if img != ".DS_Store" and img != ".anchor":
			PETREPORT_SAMPLE_BIRD_IMAGES.append("images/petreport_sample_images/bird/" + img)
	for img in os.listdir(PETREPORT_SAMPLE_HORSE_IMAGES_DIRECTORY):
		if img != ".DS_Store" and img != ".anchor":
			PETREPORT_SAMPLE_HORSE_IMAGES.append("images/petreport_sample_images/horse/" + img)
	for img in os.listdir(PETREPORT_SAMPLE_RABBIT_IMAGES_DIRECTORY):
		if img != ".DS_Store" and img != ".anchor":
			PETREPORT_SAMPLE_RABBIT_IMAGES.append("images/petreport_sample_images/rabbit/" + img)
	for img in os.listdir(PETREPORT_SAMPLE_SNAKE_IMAGES_DIRECTORY):
		if img != ".DS_Store" and img != ".anchor":
			PETREPORT_SAMPLE_SNAKE_IMAGES.append("images/petreport_sample_images/snake/" + img)
	for img in os.listdir(PETREPORT_SAMPLE_TURTLE_IMAGES_DIRECTORY):
		if img != ".DS_Store" and img != ".anchor":
			PETREPORT_SAMPLE_TURTLE_IMAGES.append("images/petreport_sample_images/turtle/" + img)

