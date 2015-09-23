from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from django import forms
from django.forms import ModelForm, Textarea
from django.template.loader import render_to_string
from django.dispatch import receiver
from registration.forms import RegistrationFormTermsOfService
from django.core.exceptions import MultipleObjectsReturned
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete, m2m_changed
from datetime import date, datetime
from utilities.utils import *
from constants import *
from home.constants import *

#The User Profile Model containing a 1-1 association with the 
#django.contrib.auth.models.User object, among other attributes.
class UserProfile (models.Model):
    '''Required Fields'''
    user = models.OneToOneField(User, null=False, default=None)    
    dob = models.DateField(null=False, default=date.today())

    '''Non-Required Fields'''
    img_path = models.ImageField(upload_to=USERPROFILE_IMG_PATH, default=USERPROFILE_IMG_PATH_DEFAULT, null=True)
    thumb_path = models.ImageField(upload_to=USERPROFILE_THUMBNAIL_PATH, default=USERPROFILE_THUMBNAIL_PATH_DEFAULT, null=True)
    last_logout = models.DateTimeField(null=True, auto_now_add=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    reputation = models.FloatField(default=0, null=True)
    description   = models.CharField(max_length=USERPROFILE_DESCRIPTION_LENGTH, null=True, default="")
    social_profile = models.BooleanField(default=False)

    #Guardian Attributes for Child Assent.
    is_minor = models.BooleanField(default=False)
    guardian_consented = models.BooleanField(default=False)
    guardian_email = models.EmailField(null=True, default=None)
    guardian_activation_key = models.CharField(null=True, max_length=40)

    def to_DICT(self):
        return {    "id"                : self.id,
                    "username"          : self.user.username,
                    "img_path"          : self.img_path.name,
                    "thumb_path"        : self.thumb_path.name,
                    "date_of_birth"     : self.dob.ctime(),
                    "last_logout"       : self.last_logout.ctime(),
                    "reputation"        : float(self.reputation),
                    "description"       : self.description,
                    "is_social_profile" : self.social_profile,
                    "is_minor"          : self.is_minor }
                    
    def send_email_message_to_UserProfile (self, target_userprofile, message, test_email=True):
        if email_is_valid(target_userprofile.user.email) or (test_email == True):
            site = Site.objects.get(pk=1)
            ctx = {"site":site, "message":message, "from_user":self.user, "from_user_profile_URL": URL_USERPROFILE + str(self.id)}
            email_body = render_to_string(TEXTFILE_EMAIL_USERPROFILE_MESSAGE, ctx)
            email_subject = "EmergencyPetMatcher: You have a new message from %s" % self.user.username

            #If test_email, just return email properties - no need to email.
            if test_email == True:
                return {"subject": email_subject, "body":email_body, "from_username": self.user.username, "to_username": target_userprofile.user.username}

            #Go ahead and email now.
            target_userprofile.user.email_user(email_subject,email_body,from_email=None)
            return True
        return False

    @staticmethod
    def get_UserProfile(profile_id=None, username=None, email=None, guardian_activation_key=None):
        try:
            if username != None:
                existing_profile = UserProfile.objects.get(user__username=username)
            elif profile_id != None:
                existing_profile = UserProfile.objects.get(pk=profile_id)
            elif email != None:
                existing_profile = UserProfile.objects.get(user__email=email)
            elif guardian_activation_key != None:
                existing_profile = UserProfile.objects.get(guardian_activation_key=guardian_activation_key)
            else:
                return None
            return existing_profile

        except MultipleObjectsReturned:
            return -1 
        except UserProfile.DoesNotExist:
            return None          

    def get_reported_PetReports(self):
        return self.proposed_related.all()

    def get_proposed_PetMatches(self):
        return self.proposed_by_related.all()

    def get_voted_PetMatches(self):
        return list(self.up_votes_related.all()) + list(self.down_votes_related.all())

    # This function accepts a RegistrationFormTermsOfService (if available) and a request POST object 
    # and attempts to validate form data. It returns (A, B), where A is a Boolean
    # that determines whether the form data validated successfully, and B the 
    # message generated by errors (where A is True).
    #
    # To check for age, This function examines the date of birth to determine if system needs 
    # to provide child assent process. It will send an email if the age is less than 18
    # and the guardian email address is valid.
    @staticmethod
    def check_registration(post_obj, registration_form=None):
        username = post_obj.get("username")
        email = post_obj.get("email")
        guardian_email = post_obj.get("guardian_email")
        dob = post_obj.get("date_of_birth")

        #Username must be unique.
        if UserProfile.get_UserProfile(username=username) != None:
            return (False, "Username has already been taken. Please try another one.")

        #Email must be unique.
        if UserProfile.get_UserProfile(email=email) != None:
            return (False, "Email has already been taken. Please try another one.")

        if is_minor(dob) == True:
            #If Minor and NO guardian email, flag it.
            if guardian_email == None:
                return (False, "You must provide a parent/guardian email to register.")
            #If email of both ppl are the same, flag it.
            elif email == guardian_email:
                return (False, "Your email address and your parent/guardian's email address cannot be the same.")

        if registration_form != None:
            if registration_form.is_valid() == False:
                # print_error_msg(registration_form.errors)
                return (False, "Errors were found in the form.")

            #Passwords must match.
            if post_obj.get("password1") != post_obj.get("password2"):
                return (False, "Passwords do not match.")               
        return (True, None)

    #Update the current user's reputation points based on an activity
    def update_reputation(self, activity):
        if activity in ACTIVITIES.keys():
            self.reputation += ACTIVITIES[activity]["reward"]
        else:
            print_error_msg("Activity %s does not exist!")

        self.save()
        return self

    #Format the DOB string ("MM/DD/YYYY") coming in and set it to DOB Attribute.
    def set_date_of_birth(self, dob_str):
        dob = map(lambda s: int(s), dob_str.split("/"))
        self.dob = date(dob[2], dob[0], dob[1])        
        self.save()

    #check if username exists in the database
    @staticmethod
    def username_exists(username):
        if User.objects.filter(username=username).count():
            return True
        return False            

    def __unicode__ (self):
         return '{ID{%s} %s}' % (self.id, self.user.username)


    #set_img_path(): Sets the image path and thumb path for this UserProfile. Save is optional.
    #Returns True if setting photo for the first time, False otherwise.
    def set_images(self, img_path, save=True, rotation=0):
        #Deal with the 'None' case.
        if img_path == None:
            self.img_path = USERPROFILE_IMG_PATH_DEFAULT
            self.thumb_path = USERPROFILE_THUMBNAIL_PATH_DEFAULT

            if save == True:
                self.save()
        else:
            #Safely open the image.
            img = open_image(img_path)
            print_debug_msg("UserProfile.set_images(): %s" % img)

            if save == True:
                #Save first - we must have the UserProfile ID.
                self.img_path = None
                self.thumb_path = None
                self.save()

                #Make this unique to prevent any image overwrites when saving a picture for a UserProfile.
                unique_img_name = str(self.id) + "-" + self.user.username + ".jpg"

                #Perform rotation (if it applies)
                img = img.rotate(rotation)
                self.img_path = USERPROFILE_IMG_PATH + unique_img_name
                self.thumb_path = USERPROFILE_THUMBNAIL_PATH + unique_img_name                    
                img.save(USERPROFILE_UPLOADS_DIRECTORY + unique_img_name, "JPEG", quality=75)
                img.thumbnail((USERPROFILE_THUMBNAIL_WIDTH, USERPROFILE_THUMBNAIL_HEIGHT), Image.ANTIALIAS)
                img.save(USERPROFILE_THUMBNAILS_DIRECTORY + unique_img_name, "JPEG", quality=75)

                #Save again.
                self.save()
            else:
                self.img_path = img_path
                self.thumb_path = img_path  


class EditUserProfile(models.Model):
    user = models.OneToOneField(User, null=False, default=None)
    activation_key = models.CharField(max_length=40,null=True)
    date_of_change = models.DateTimeField(default=timezone.now)
    new_email = models.EmailField(null=True)

    def activation_key_expired(self):
        expiration_date = timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        if (self.date_of_change + expiration_date) >= datetime.now():
            return False
        return True



#The UserProfile Form - used for editing the user profile
#edit initial value of each field either in the view or in the template
class UserProfileForm (ModelForm):
    #Required Fields
    username = forms.CharField(label="Username", max_length=USER_USERNAME_LENGTH, required=True) 
    email = forms.EmailField(label="Email", required=True)

    #Non-Required Fields
    first_name = forms.CharField(label="First Name", max_length=USER_FIRSTNAME_LENGTH, required=False)
    last_name = forms.CharField(label="Last Name", max_length=USER_LASTNAME_LENGTH, required=False)
    description  = forms.CharField(label="Describe Yourself", max_length=USERPROFILE_DESCRIPTION_LENGTH, widget=forms.Textarea, required=False)
    photo = forms.ImageField(label="Profile Picture", help_text="(*.jpg, *.png, *.bmp), 3MB maximum", widget=forms.ClearableFileInput, required=False)

    class Meta:
        model = UserProfile
        #exclude = ('revision_number', 'workers', 'proposed_by','bookmarked_by','closed', 'thumb_path')
        fields = ("username", "first_name", "last_name", "email", "photo")


#Create a pre-delete signal function to delete a UserProfile before a User/UserProfile is deleted
@receiver (pre_delete, sender=UserProfile)
def delete_UserProfile(sender, instance=None, **kwargs):
    if instance.user == None:
        print_error_msg("User was deleted before UserProfile. Cannot delete log file.")
    else:    
        #Instead of deleting the User (which might break foreign-key relationships),
        #set the active flag to False (INACTIVE)
        instance.user.is_active = False
        instance.user.save()

from home.models import Activity
#Create a post save signal function to setup a UserProfile when a User is created
@receiver (post_save, sender=User)
def setup_UserProfile(sender, instance, created, **kwargs):
    if created == True:
        userprofile = UserProfile.objects.create(user=instance)
        Activity.log_activity("ACTIVITY_ACCOUNT_CREATED", userprofile)
        userprofile.update_reputation("ACTIVITY_ACCOUNT_CREATED")

