from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete, m2m_changed
from django.dispatch import receiver
from django.core.files.storage import FileSystemStorage
import PIL, os, time
from django import forms
from constants import *
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.timezone import now as datetime_now
from datetime import timedelta
from django.conf import settings

'''===================================================================================
[models.py]: Models for the EPM system
==================================================================================='''

'''Enums for Various Model Choice Fields'''
PET_TYPE_CHOICES = [('Dog', 'Dog'), ('Cat', 'Cat'), ('Turtle', 'Turtle'), ('Snake', 'Snake'), ('Horse', 'Horse'),('Rabbit', 'Rabbit'), ('Other', 'Other')]
STATUS_CHOICES = [('Lost','Lost'),('Found','Found')]
SEX_CHOICES=[('M','Male'),('F','Female')]
SIZE_CHOICES = [('L', 'Large (100+ lbs.)'), ('M', 'Medium (10 - 100 lbs.)'), ('S', 'Small (0 - 10 lbs.)')]
BREED_CHOICES = [('Scottish Terrier','Scottish Terrier'),('Golden Retriever','Golden Retriever'),('Yellow Labrador','Yellow Labrador')]

#The User Profile Model containing a 1-1 association with the 
#django.contrib.auth.models.User object, among other attributes.
class UserProfile (models.Model):

    '''Required Fields'''
    user = models.OneToOneField(User, null=False, default=None)
    photo = models.ImageField(upload_to='images/profile_images', null=True) 
    '''Non-Required Fields'''
    last_logout = models.DateTimeField(null=True, auto_now_add=True)
    following = models.ManyToManyField('self', null=True, symmetrical=False, related_name='followers')
    is_test = models.BooleanField(default=False)
    chats = models.ManyToManyField('Chat', null=True)
    reputation = models.FloatField(default=0, null=True)
    # facebook_cred = models.CharField(max_length=100, null=True)
    # twitter_cred = models.CharField(max_length=100, null=True)
    #facebook_id = models.IntegerField(blank=True, null=True)
    #twitter_id = models.IntegerField(blank=True, null=True)

    #Create the activity log for this user
    def set_activity_log(self, is_test=False):
        if is_test == True:
            self.is_test = True
            print "[OK]: A new UserProfile TEST log file was created for {%s} with ID{%d}\n" % (self.user.username, self.id)                        
        else:
            self.is_test = False
            print "[OK]: A new UserProfile log file was created for {%s} with ID{%d}\n" % (self.user.username, self.id)                        

        self.save()
        log_activity(ACTIVITY_ACCOUNT_CREATED, self)

    #check if username exists in the database
    @staticmethod
    def username_exists(username):
        if User.objects.filter(username=username).count():
            return True
        return False            

    def __unicode__ (self):
         return '{ID{%s} %s}' % (self.id, self.user.username)


class PetReport(models.Model):

    '''Required Fields'''
    pet_type = models.CharField(max_length=PETREPORT_PET_TYPE_LENGTH, choices = PET_TYPE_CHOICES, null=False, default=None)
    status = models.CharField(max_length = PETREPORT_STATUS_LENGTH, choices = STATUS_CHOICES, null=False, default=None)
    date_lost_or_found = models.DateField(null=False)
    sex = models.CharField(max_length=PETREPORT_SEX_LENGTH, choices=SEX_CHOICES, null=False)
    size = models.CharField(max_length=PETREPORT_SIZE_LENGTH, choices = SIZE_CHOICES, null=False)
    location = models.CharField(max_length=PETREPORT_LOCATION_LENGTH, null=False, default='unknown')

    #ForeignKey: Many-to-one relationship with User
    proposed_by = models.ForeignKey('UserProfile', null=False, default=None)

    '''Non-Required Fields'''
    img_path = models.ImageField(upload_to='images/petreport_images', null=True)
    pet_name = models.CharField(max_length=PETREPORT_PET_NAME_LENGTH, null=True, default='unknown') 
    age = models.CharField(max_length=PETREPORT_AGE_LENGTH, null=True, default= 'unknown')
    color = models.CharField(max_length=PETREPORT_COLOR_LENGTH, null=True,default='unknown')
    breed = models.CharField(max_length=PETREPORT_BREED_LENGTH, null=True,default='unknown')
    revision_number = models.IntegerField(null=True) #update revision using view
    description   = models.CharField(max_length=PETREPORT_DESCRIPTION_LENGTH, null=True, default="")
    #Many-to-Many relationship with User
    workers = models.ManyToManyField('UserProfile', null=True, related_name='workers_related')
    bookmarked_by = models.ManyToManyField('UserProfile', null=True, related_name='bookmarks_related')

    #Override the save method for this model
    def save(self, *args, **kwargs):

        if self.id == None:
            print "%s has been saved!" % self
        else:
            print "%s has been updated!" % self

        super(PetReport, self).save(args, kwargs)            
        return self

    ''' Determine if the input UserProfile (user) has bookmarked this PetReport already '''
    def UserProfile_has_bookmarked(self, user_profile):
        assert isinstance(user_profile, UserProfile)
        try:
            user = self.bookmarked_by.get(pk = user_profile.id)
        except UserProfile.DoesNotExist:
            user = None        
        if (user != None):
            return True
        else:
            return False
        return False

    @staticmethod
    def get_PetReport(status, pet_type, pet_name=None, petreport_id=None):

        try:
            if petreport_id != None:
                existing_pet = PetReport.objects.get(pk=petreport_id)
            elif pet_name != None:
                existing_pet = PetReport.objects.get(status=status, pet_type=pet_type, pet_name=pet_name)
            else:
                existing_pet = PetReport.objects.get(status=status, pet_type=pet_type)

            return existing_pet

        except PetReport.DoesNotExist:
            return None

    def has_image(self):
        if self.img_path == None:
            return False
        return True

    def __unicode__(self):
        return '{ID{%s} %s %s name:%s}' % (self.id, self.status, self.pet_type, self.pet_name)

    def long_unicode (self):
        str = "PetReport {\n\tpet_type: %s\n\tstatus: %s\n\tproposed_by: %s\n\t" % (self.pet_type, self.status, self.proposed_by)
        str += "date_lost_or_found: %s\n\tsex: %s\n\tsize: %s\n\tlocation: %s\n\t" % (self.date_lost_or_found, self.sex, self.size, self.location)
        str += "age: %s\n\tbreed: %s\n\tdescription: %s\n\t}" % (self.age, self.breed, self.description)
        return str

    def convert_date_to_string(self):
        string = str(self.date_lost_or_found)
        return str


#The Pet Match Object Model
class PetMatch(models.Model):

    '''Required Fields'''
    lost_pet = models.ForeignKey('PetReport', null=False, default=None, related_name='lost_pet_related')
    found_pet = models.ForeignKey('PetReport', null=False, default=None, related_name='found_pet_related')
    proposed_by = models.ForeignKey('UserProfile', null=False, related_name='proposed_by_related')
    proposed_date = models.DateTimeField(null=False, auto_now_add=True)
    description = models.CharField(max_length=PETMATCH_DESCRIPTION_LENGTH, null=False, default=None)
    '''Non-Required Fields'''
    '''is_open will be set to False once it is triggered for verification i.e., it will not be available
    to the crowd for viewing/voting after this petmatch triggers the verification workflow or if it is 
    declared as a Failed PetMatch when a successful PetMatch is found for either of the PetReports associated with
    the current Petmatch instance'''
    is_open = models.BooleanField(default=True)
    is_successful = models.BooleanField(default=False)
    '''verification_triggered will be set to true if and when a PetMatch reaches the 
    threshold for verification'''
    verification_triggered = models.BooleanField(default=False)
    score = models.IntegerField(default=0)
    #closed_by = models.ForeignKey('UserProfile', null=True, related_name='closed_by_related')
    '''closed_date is the date when the PetMatch is closed for good (after verification)'''
    closed_date = models.DateTimeField(null=True)
    up_votes = models.ManyToManyField('UserProfile', null=True, related_name='up_votes_related')
    down_votes = models.ManyToManyField('UserProfile', null=True, related_name='down_votes_related')
    '''verification_votes represents user responses sent via the verify_petmatch webpage.
    the first bit holds the Lost Contact's response and the second bit holds the 
    Found Contact's response. 
    0 - No response was recorded
    1 - user clicked on Yes
    2 - User clicked on No'''
    verification_votes = models.CharField(max_length=PETMATCH_VERIFICATION_VOTES_LENGTH,default='00')

    '''Because of the Uniqueness constraint that the PetMatch must uphold, we override the save method'''
    def save(self, *args, **kwargs):
        #First, try to find an existing PetMatch
        lost_pet = self.lost_pet
        found_pet = self.found_pet
        
        #PetMatch inserted improperly
        if (lost_pet.status != "Lost") or (found_pet.status != "Found"):
            print "[ERROR]: The PetMatch was not saved because it was inserted improperly. Check to make sure that the PetMatch consists of one lost and found pet and that they are being assigned to the lost and found fields, respectively."
            return (None, "INSERTED IMPROPERLY")

        existing_match = PetMatch.get_PetMatch(self.lost_pet, self.found_pet)            

        #A PetMatch with the same lost and found pets (and same user who proposed it) already exists - SQL Update
        if existing_match != None:
            if existing_match.id == self.id:
                super(PetMatch, self).save(args, kwargs)
                print "[SQL UPDATE]: %s" % self
                return (self, "SQL UPDATE")
            else:
                print "[DUPLICATE PETMATCH]: %s VS. %s" % (self, existing_match)
                return (None, "DUPLICATE PETMATCH") #Duplicate PetMatch!

        #Good to go: Save the PetMatch Object.
        super(PetMatch, self).save(*args, **kwargs)
        print "[OK]: PetMatch %s was saved!" % self
        return (self, "NEW PETMATCH")


    ''' Determine if a PetMatch exists between pr1 and pr2, and if so, return it. Otherwise, return None. '''
    @staticmethod
    def get_PetMatch(pr1, pr2):
        assert isinstance(pr1, PetReport)
        assert isinstance(pr2, PetReport)

        try:
            if pr1.status == "Lost":
                existing_match = PetMatch.objects.get(lost_pet = pr1, found_pet = pr2)
            else:
                existing_match = PetMatch.objects.get(lost_pet = pr2, found_pet = pr1)

            return existing_match

        except PetMatch.DoesNotExist:
            return None

    ''' Determine if the input UserProfile (user) has up/down-voted on this PetMatch already '''
    def UserProfile_has_voted(self, user_profile):
        assert isinstance(user_profile, UserProfile)

        try:
            upvote = self.up_votes.get(pk = user_profile.id)
        except UserProfile.DoesNotExist:
            upvote = None
        try:
            downvote = self.down_votes.get(pk = user_profile.id)
        except UserProfile.DoesNotExist:
            downvote = None

        if (upvote != None):
            return UPVOTE
        elif (downvote != None):
            return DOWNVOTE

        return False      
    def PetMatch_has_reached_threshold(self):
        '''Difference[D] is calculated as the difference between number of upvotes and number of downvotes. 
        For a PetMatch to be successful, it should satisfy certain constraints. D should exceed a threshold value,
        which is half the number of active users on the system. '''
        active_users = 10 
        '''10 will be replaced by a function that returns the number of active users in the system'''
        threshold = active_users/2 
        difference = self.up_votes.count() - self.down_votes.count()
        if difference >= threshold:
            return True
        else:
            return False

    #Change this to verify_PetMatch
    def verify_petmatch(self):
        self.is_open = False
        self.verification_triggered = True
        self.save()
        print '[INFO]: PetMatch is now closed to the crowd, verification has been triggered'
        petmatch_owner = self.proposed_by.user
        lost_pet_contact = self.lost_pet.proposed_by.user
        found_pet_contact = self.found_pet.proposed_by.user
        if petmatch_owner.username == lost_pet_contact.username or petmatch_owner.username == found_pet_contact.username: 
            Optionally_discuss_with_digital_volunteer = ""
        else:
            Optionally_discuss_with_digital_volunteer = "You may also discuss this pet match with %s, the digital volunteer who proposed this pet match. You can reach %s at %s" % (self.proposed_by.user.username,self.proposed_by.user.username,self.proposed_by.user.email)
        '''An email is sent to the lost pet owner'''
        ctx = {'pet_type':'your lost pet','opposite_pet_type_contact':found_pet_contact,'pet_status':"found",'Optionally_discuss_with_digital_volunteer':Optionally_discuss_with_digital_volunteer,"petmatch_id":self.id}
        email_body = render_to_string(TEXTFILE_EMAIL_PETOWNER_VERIFY_PETMATCH,ctx)
        email_subject = EMAIL_SUBJECT_PETOWNER_VERIFY_PETMATCH
        if not lost_pet_contact.get_profile().is_test:
            lost_pet_contact.email_user(email_subject,email_body,from_email=None)
        print '[INFO]: Email to lost pet owner: '+email_body
        ''' An email is sent to the found pet owner '''
        ctx = {'pet_type':'the pet you found','opposite_pet_type_contact':lost_pet_contact,'pet_status':"lost",'Optionally_discuss_with_digital_volunteer':Optionally_discuss_with_digital_volunteer,"petmatch_id":self.id}
        email_body = render_to_string(TEXTFILE_EMAIL_PETOWNER_VERIFY_PETMATCH,ctx)
        email_subject = EMAIL_SUBJECT_PETOWNER_VERIFY_PETMATCH
        if not found_pet_contact.get_profile().is_test:
            found_pet_contact.email_user(email_subject,email_body,from_email=None)
        print '[INFO]: Email to found pet owner: '+email_body
       
        '''If the pet match was proposed by a person other than the lost_pet_contact/found_pet_contact,
        an email will be sent to this person '''
        if Optionally_discuss_with_digital_volunteer != "":
            ctx = { 'lost_pet_contact':lost_pet_contact,'found_pet_contact':found_pet_contact }
            email_body = render_to_string(TEXTFILE_EMAIL_PETMATCH_PROPOSER,ctx)
            email_subject =  EMAIL_SUBJECT_PETMATCH_PROPOSER  
            if not petmatch_owner.get_profile().is_test:
                petmatch_owner.email_user(email_subject,email_body,from_email=None)
            print '[INFO]: Email to pet match owner: '+email_body

    def close_PetMatch(self):
        if '0' not in self.verification_votes:
            self.closed_date = datetime_now()         
            '''If the PetMatch is successful, all related PetMatches will be closed 
            and is_successful is set to True'''
            if self.verification_votes == '11':
                self.is_successful = True
                for petmatch in self.lost_pet.lost_pet_related.all(): 
                    petmatch.is_open = False
                    petmatch.closed_date = datetime_now()
                    petmatch.save()
                for petmatch in self.found_pet.found_pet_related.all():
                    petmatch.is_open = False
                    petmatch.closed_date = datetime_now()
                    petmatch.save()
            self.save()    
            print '[INFO]: PetMatch %s has been closed' % (self)
    
    def __unicode__ (self):
        return '{ID{%s} lost:%s, found:%s, proposed_by:%s}' % (self.id, self.lost_pet, self.found_pet, self.proposed_by)


#The Chat Object Model
class Chat (models.Model):

    '''Required Fields'''
    #One-to-One relationship with PetReport
    pet_report = models.OneToOneField('PetReport', null=False, default=None)

    def __unicode__ (self):
        return 'Chat {pet_report:%s}' % (self.pet_report)


#The Chat Line Object Model
class ChatLine (models.Model):

    '''Required Fields'''
    chat = models.ForeignKey('Chat', null=False, default=None)
    userprofile = models.ForeignKey('UserProfile', null=False, default=None)
    text = models.CharField (max_length=CHATLINE_TEXT_LENGTH, blank=True, null=False, default=None)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__ (self):
        return 'ChatLine {text:%s}' % (self.text)



''' ============================ [FORM MODELS] ==================================== '''
''' These Models nicely organize the model-related data into Django Form objects that 
    have built-in validation functionality and can be passed around via POST requests. 
    Order of Fields matter.                                                         '''


#The PetReport ModelForm
class PetReportForm (ModelForm):
    '''Required Fields'''
    pet_type = forms.ChoiceField(label = 'Pet Type', choices = PET_TYPE_CHOICES, required = True)
    status = forms.ChoiceField(label = "Status (Lost/Found)", choices = STATUS_CHOICES, required = True)
    date_lost_or_found = forms.DateField(label = "Date Lost/Found", required = True)
    sex = forms.ChoiceField(label = "Sex", choices = SEX_CHOICES, required = True)
    size = forms.ChoiceField(label = "Size of Pet", choices = SIZE_CHOICES, required = True)
    location = forms.CharField(label = "Location", max_length = PETREPORT_LOCATION_LENGTH , required = True)

    '''Non-Required Fields'''
    img_path = forms.ImageField(label = "Upload an Image (*.jpg, *.png, *.bmp, *.tif)", required = False)
    pet_name = forms.CharField(label = "Pet Name", max_length=PETREPORT_PET_NAME_LENGTH, required = False) 
    age = forms.CharField(label = "Age", max_length = PETREPORT_AGE_LENGTH, required = False)
    breed = forms.CharField(label = "Breed", max_length = PETREPORT_BREED_LENGTH, required = False)
    color = forms.CharField(label = "Coat Color(s)", max_length = PETREPORT_COLOR_LENGTH, required = False)
    description  = forms.CharField(label = "Description", max_length = PETREPORT_DESCRIPTION_LENGTH, required = False, widget = forms.Textarea)

    class Meta:
        model = PetReport
        exclude = ('revision_number', 'workers', 'proposed_by','bookmarked_by')

#The UserProfile Form - used for editing the user profile
#edit initial value of each field either in the view or in the template
class UserProfileForm (forms.Form):
    '''Required Fields'''
    username = forms.CharField(label="Username*",max_length=30) 
    '''Non-Required Fields'''
    first_name = forms.CharField(label="First Name",max_length=30,required=False)
    last_name = forms.CharField(label="Last Name",max_length=30,required=False)
    email = forms.EmailField(label="Email*",required=False)
    old_password = forms.CharField(label="Old Password",max_length=30,widget = forms.PasswordInput,required=False) 
    new_password = forms.CharField(label="New Password",max_length=30,widget = forms.PasswordInput,required=False) 
    confirm_password = forms.CharField(label="Confirm Password",max_length=30,widget = forms.PasswordInput,required=False) 
    photo = forms.ImageField(label="Profile Picture", required=False)


class EditUserProfile(models.Model):
    user = models.OneToOneField(User,null=False,default=None)
    activation_key = models.CharField(max_length=40,null=True)
    date_of_change = models.DateTimeField(default=timezone.now)
    new_email = models.EmailField(null=True)
    def activation_key_expired(self):
        """ADAPTED FROM DJANGO-REGISTRATION: https://bitbucket.org/ubernostrum/django-registration

        Determine whether this activation key has expired, 
        returning a boolean -- ``True`` if the key
        has expired.
        
        Key expiration is determined by a two-step process:
        
        1. If the user has already activated his new email, 
           the key will have been reset to the string constant 
           ``ACTIVATED``. Re-activating is not permitted, and so 
           this method returns ``True`` in this case.

        2. Otherwise, the date the user changed his email is incremented by
           the number of days specified in the setting
           ``ACCOUNT_ACTIVATION_DAYS`` (which should be the number of
           days after change of email during which a user is allowed to
           activate their account); if the result is less than or
           equal to the current date, the key has expired and this
           method returns ``True``.
        
        """
        expiration_date = timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == "ACTIVATED" or (self.date_of_change + expiration_date <= datetime_now())
    activation_key_expired.boolean = True

''' ============================ [SIGNALS] ==================================== '''

#Create a pre-delete signal function to delete a UserProfile before a User/UserProfile is deleted
@receiver (pre_delete, sender=UserProfile)
def delete_UserProfile(sender, instance=None, **kwargs):
    if instance.user == None:
        print "[ERROR]: User was deleted before UserProfile. Cannot delete log file."

    else:    
        #Delete the UserProfile log file.
        delete_log(instance)
        #Instead of deleting the User (which might break foreign-key relationships),
        #set the active flag to False (INACTIVE)
        instance.user.is_active = False
        instance.user.save()

#Create a post save signal function to setup a UserProfile when a User is created
@receiver (post_save, sender=User)
def setup_UserProfile(sender, instance, created, **kwargs):
    if created == True:
        #Create a UserProfile object.
        UserProfile.objects.create(user=instance)

#Post Add Signal function to check if a PetMatch has reached threshold
@receiver(m2m_changed, sender=PetMatch.up_votes.through)
def trigger_PetMatch_verification(sender, instance,action,**kwargs):
    '''Checking condition that will return true once PetMatch reaches a threshold value,
    if it returns true, pet match verification work flow is triggered'''
    #print 'trigger_PetMatch_verification sign triggered'
    if action == 'post_add':
        if instance.PetMatch_has_reached_threshold():
            print '[INFO]: PetMatch has reached the threshold'
            instance.verify_petmatch()   
            instance.save()

''' Import statements placed at the bottom of the page to prevent circular import dependence '''
from logging import *
