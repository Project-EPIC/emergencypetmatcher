import os
from project.settings import STATIC_URL

#Number of Tests
NUMBER_OF_TESTS = 10

#URLS - use for redirect calls
URL_HOME = '/'
URL_GET_ACTIVITIES = "/get_activities_json"
URL_GET_BOOKMARKS = "/get_bookmarks"
URL_LOGIN = '/login'
URL_REGISTRATION = "/accounts/register/"
URL_REGISTRATION_COMPLETE = "/register/complete/"
URL_ACTIVATION_COMPLETE = "/accounts/activate/complete/"
URL_SOCIAL_AUTH_GET_DETAILS = "/social_auth_get_details"
URL_SOCIAL_AUTH_COMPLETE = "/complete/"


#HTML File Paths (relative to STATIC_URL) - use for render_to_response calls
HTML_HOME = "home/index.html"
HTML_BOOKMARKS = "home/bookmarks.html"
HTML_ABOUT = "home/about.html"
HTML_LOGIN = "home/login.html"
HTML_REGISTRATION_FORM = "registration/register.html"
HTML_SOCIAL_AUTH_FORM = "registration/social_auth_form.html"


#E-mail Constants
EMAIL_SUBJECT_PETMATCH_PROPOSER='EmergencyPetMatcher: Your pet match is close to being successful!'
TEST_EMAIL="emergencypetmatchertest@gmail.com"

#Email Change.
TEXTFILE_EMAIL_CHANGE_BODY = "socializing/email_change_body.txt"
TEXTFILE_EMAIL_CHANGE_SUBJECT = "socializing/email_change_subject.txt"

TEXTFILE_EMAIL_PETMATCH_PROPOSER = "matching/verification_email_to_digital_volunteer.txt"
TEXTFILE_EMAIL_USERPROFILE_MESSAGE = "socializing/email_message_user.txt"
TEXTFILE_EMAIL_GUARDIAN_SUBJECT = "registration/guardian_email_subject.txt"
TEXTFILE_EMAIL_GUARDIAN_BODY = "registration/guardian_email.txt"


#General File Path Constants
PROJECT_WORKSPACE = os.path.dirname(__file__)
EPM_DIRECTORY = os.path.dirname(PROJECT_WORKSPACE)
LOGS_DIRECTORY = STATIC_URL + "logs/"

#Represents how many activities to fetch per request.
ACTIVITY_FEED_LENGTH = 10

#Activity Log File Path Constants
ACTIVITY_LOG_DIRECTORY = LOGS_DIRECTORY + "activity_logs/"

#Activities with their reward points attached.
ACTIVITIES = {  "ACTIVITY_ACCOUNT_CREATED"            : {"reward": 10},
                "ACTIVITY_LOGIN"                      : {"reward":  0},
                "ACTIVITY_LOGOUT"                     : {"reward":  0},
                "ACTIVITY_USER_CHANGED_USERNAME"      : {"reward":  0},
                "ACTIVITY_USER_SET_PHOTO"             : {"reward":  2},
                "ACTIVITY_PETREPORT_SUBMITTED"        : {"reward": 10},
                "ACTIVITY_PETREPORT_ADD_BOOKMARK"     : {"reward":  0},
                "ACTIVITY_PETREPORT_REMOVE_BOOKMARK"  : {"reward":  0},
                "ACTIVITY_PETMATCH_PROPOSED"          : {"reward": 15},
                "ACTIVITY_PETMATCH_UPVOTE"            : {"reward":  1},
                "ACTIVITY_PETMATCH_DOWNVOTE"          : {"reward":  1},
                "ACTIVITY_PETCHECK_VERIFY"            : {"reward":  5},
                "ACTIVITY_PETCHECK_VERIFY_SUCCESS"    : {"reward": 20},
                "ACTIVITY_PETCHECK_VERIFY_FAIL"       : {"reward": 10},
                "ACTIVITY_SOCIAL_FOLLOW"              : {"reward":  5},
                "ACTIVITY_SOCIAL_UNFOLLOW"            : {"reward":  0},
                "ACTIVITY_SOCIAL_SEND_MESSAGE_TO_USER": {"reward":  0}  }

ACTIVITY_SOCIAL_ACTIVITIES = ["ACTIVITY_ACCOUNT_CREATED",
                              "ACTIVITY_USER_CHANGED_USERNAME",
                              "ACTIVITY_USER_SET_PHOTO",
                              "ACTIVITY_PETREPORT_SUBMITTED," 
                              "ACTIVITY_PETMATCH_PROPOSED," 
                              "ACTIVITY_PETMATCH_UPVOTE," 
                              "ACTIVITY_PETMATCH_DOWNVOTE",
                              "ACTIVITY_PETCHECK_VERIFY",
                              "ACTIVITY_PETCHECK_VERIFY_SUCCESS",
                              "ACTIVITY_PETCHECK_VERIFY_FAIL",
                              "ACTIVITY_SOCIAL_FOLLOW"]

#Activity Model Field Length
ACTIVITIES_MAX_LENGTH = 50                              


TOS_MINOR_TEXT = """Hello! We are researchers from Project EPIC (Empowering the Public with Information in Crisis) at the University of Colorado Boulder.  We are doing a study to see how excellent volunteers like you work with each other to help pet owners find their pets when disaster strikes. We are asking you to take part in the research study because we are interested in how you use EmergencyPetMatcher.

For this research, we will keep track of the information you provide to us, like the pets and pet matches you work on, which users you talk to, and how often you log on and use EPM. We will keep all of your information secure and private as much as possible. Some information, such as your username, needs to be public so others on the web site know who you are. 

We are asking that you provide one of your parent's email address below to make sure that they are okay with you using EmergencyPetMatcher. If you check the box below, it means that you have read this and that you want to be in the study. If you don't want to be in the research, don't click the box. Being in this research is up to you, and no one will be upset if you don't check the box, or if you change your mind later. If you check the box, and your parent/guardian also provides consent on the email they will have received, then you will be able to use EmergencyPetMatcher. You won't be able to register for EmergencyPetMatcher until we receive your parent's consent as well as yours.

We're super excited for you to take part and volunteer to help report and match lost and found pets. Let's get these pets back home!
 
You should know that:
- You do not have to be in this study if you do not want to.  You won't get into any trouble if you say no.
- Your parent(s)/guardian(s) were asked if it is OK for you to be in this study.  Even if they say it's OK, it is still your choice whether or not to take part. 
- You can ask any questions you have, now or later.  If you think of a question later, you or your parents can contact us at emergencypetmatcher-support@googlegroups.com. Keep this email address so you can refer to it later.
 
Sign this form only if you:
- understand what you will be doing for this study,
- have all your questions answered,
- have talked to your parent(s)/legal guardian about this project, and agree to take part in this research.

Thanks!
Project EPIC
"""

TOS_ADULT_TEXT = """Welcome to EmergencyPetMatcher! By checking the box below you indicate that you have read, understood, and agreed to the following:
 
Emergency Pet Matcher (EPM) is a tool developed and supported by the Project EPIC (Empowering the Public with Information in Crisis) research team at the University of Colorado Boulder. This research project is led by Leysia Palen (Professor of the Department of Computer Science, 430 UCB, palen@cs.colorado.edu).
 
Project Description: This project studies how people collect and share information about displaced pets in disaster events.
 
Procedures: Researchers will observe your engagement with Emergency Pet Matcher and with other users while you are using both the public and private aspects of the EPM system. The researchers may reach out to you via email and enquire whether you would be willing to be involved in additional research such as questionnaires or interviews. Use of EPM does not compel you to participate in any such research. In all cases, when analyzing and reporting data gathered through EPM and any questionnaires or interviews you may choose to be part of, any personal information will be de-identified.
 
Risks: There are no foreseeable risks in using EPM. Please be aware the system is public - treat all content you provide and actions you take in the system to be public, including your use of the Private Message functions.
 
Benefits: There are no direct benefits to you from taking part in Emergency Pet Matcher.
 
Privacy: You have the right to withdraw consent or stop participating at any time.
We will maintain the privacy of your data and not share it with anyone outside this research group. In any research conducted we will use a pseudonym instead of your real name or EPM handle.
 
Logs of use will be kept securely within the research project's offices indefinitely, and will only be accessed by those directly working on the project. All engagement on the front end of EPM will be public.
 
Invitation for Questions: If you have questions about this study, you may contact the EPM researchers at emergencypetmatcher-support@googlegroups.com before indicating your consent. If you have questions regarding your rights as a participant, any concerns about this project, or any dissatisfaction with any aspect of this study, you may report them - confidentially, if you wish - to the Institutional Review Board, 3100 Marine Street, Rm A15, 563 UCB, ph (303) 735-3702.
 
Following your agreement below, we take your ongoing use of the system to indicate your ongoing consent. 

Thanks!
Project EPIC
"""



