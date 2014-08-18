from project.settings import MEDIA_ROOT

#URLs
URL_USERPROFILE = '/users/'
URL_SEND_MESSAGE_TO_USERPROFILE = "/users/message_UserProfile"
URL_FOLLOW = "/users/follow"
URL_UNFOLLOW = "/users/unfollow"
URL_EDITUSERPROFILE_INFO = "/users/edit_userprofile/update_User_info"
URL_EDITUSERPROFILE_PWD = "/users/edit_userprofile/update_User_password"
URL_EDITUSERPROFILE = "/users/edit_userprofile"
URL_EMAIL_VERIFICATION_COMPLETE = "/users/email_verification_complete/" 

HTML_USERPROFILE = "socializing/userprofile.html"
HTML_EDITUSERPROFILE_FORM ="socializing/edituserprofile_form.html"

#Number of Tests
NUMBER_OF_TESTS = 50

#max_length for Model Fields
USER_USERNAME_LENGTH = 30
USER_FIRSTNAME_LENGTH = 30
USER_LASTNAME_LENGTH = 30
USER_PASSWORD_LENGTH = 30
USERPROFILE_DESCRIPTION_LENGTH = 300

#Small List of Names
USER_NAMES = ['Jacob', 'Emily', 'Joshua', 'Madison', 'Kenneth', 'Mark', 'Dave', 'Angela', 'Matthew', 'Olivia', 'Daniel', 'James', 'Nicholas', 'Greg', 'Robert', 'Hannah', 'Chris', 'Abby', 'Andrew', 'Isabella', 'Mario', 'Sahar', 'Amrutha', 'Leysia', 'Ken', 'Abe']

USERPROFILE_THUMBNAIL_WIDTH = 128
USERPROFILE_THUMBNAIL_HEIGHT = 128

#UserProfile Image Paths
USERPROFILE_IMG_PATH = "userprofile/uploads/"
USERPROFILE_IMG_PATH_DEFAULT = "userprofile/uploads/defaults/anonymous.gif"
USERPROFILE_THUMBNAIL_PATH = "userprofile/thumbnails/"
USERPROFILE_THUMBNAIL_PATH_DEFAULT = "userprofile/thumbnails/defaults/anonymous.gif"

#UserProfile File Path Constants
USERPROFILE_MEDIA_DIRECTORY = MEDIA_ROOT + "userprofile/"

#Top-level UserProfile subdirectory constants
USERPROFILE_UPLOADS_DIRECTORY = USERPROFILE_MEDIA_DIRECTORY + "uploads/"
USERPROFILE_THUMBNAILS_DIRECTORY = USERPROFILE_MEDIA_DIRECTORY + "thumbnails/"
USERPROFILE_UPLOADS_DEFAULTS_DIRECTORY = USERPROFILE_UPLOADS_DIRECTORY + "defaults/"
USERPROFILE_THUMBNAILS_DEFAULTS_DIRECTORY = USERPROFILE_THUMBNAILS_DIRECTORY + "defaults/"

#Defaults
USERPROFILE_UPLOADS_DEFAULTS_IMAGE = USERPROFILE_UPLOADS_DEFAULTS_DIRECTORY + "anonymous.gif"
USERPROFILE_THUMBNAILS_DEFAULT_IMAGE = USERPROFILE_THUMBNAILS_DEFAULTS_DIRECTORY + "anonymous.gif"


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


