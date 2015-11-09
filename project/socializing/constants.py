from project.settings import MEDIA_ROOT

#URLs
URL_USERPROFILE = '/users/'
URL_SEND_MESSAGE_TO_USER = "/users/message"
URL_FOLLOW = "/users/follow"
URL_UNFOLLOW = "/users/unfollow"
URL_EDITUSERPROFILE_INFO = "/users/edit/update_info"
URL_EDITUSERPROFILE_PWD = "/users/edit/update_password"
URL_EDITUSERPROFILE = "/users/edit/"
URL_EMAIL_VERIFICATION_COMPLETE = "/users/email_verification_complete/"

HTML_USERPROFILE = "socializing/userprofile.html"
HTML_EDITUSERPROFILE_FORM ="socializing/edit_userprofile.html"

#max_length for Model Fields
USER_USERNAME_LENGTH = 30
USER_FIRSTNAME_LENGTH = 30
USER_LASTNAME_LENGTH = 30
USER_PASSWORD_LENGTH = 30
USERPROFILE_DESCRIPTION_LENGTH = 300

#Small List of Names
USER_NAMES = ['Jacob', 'Emily', 'Joshua', 'Madison', 'Kenneth', 'Mark', 'Dave', 'Angela',
'Matthew', 'Olivia', 'Daniel', 'James', 'Nicholas', 'Greg', 'Robert', 'Hannah', 'Chris',
'Abby', 'Andrew', 'Isabella', 'Mario', 'Sahar', 'Amrutha', 'Leysia', 'Ken', 'Abe']

#How big messages should be.
USERPROFILE_MESSAGE_LENGTH=1000

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
