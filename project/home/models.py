from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete
from django.dispatch import receiver
from django.core.files.storage import FileSystemStorage
import PIL, os, time
from constants import *

'''===================================================================================
[models.py]: Models for the EPM system
==================================================================================='''

'''Enums for Various Model Choice Fields'''
PET_TYPE_CHOICES = [('Dog', 'Dog'), ('Cat', 'Cat'), ('Turtle', 'Turtle'), ('Snake', 'Snake'), ('Horse', 'Horse'),('Rabbit', 'Rabbit'), ('Other', 'Other')]
STATUS_CHOICES = [('Lost','Lost'),('Found','Found')]
SEX_CHOICES=[('M','Male'),('F','Female')]
SIZE_CHOICES = [('L', 'Large (100+ lbs.)'), ('M', 'Medium (10 - 100 lbs.)'), ('S', 'Small (0 - 10 lbs.)')]
BREED_CHOICES = [('Scottish Terrier','Scottish Terrier'),('Golden Retriever','Golden Retriever'),('Yellow Labrador','Yellow Labrador')]

class PetReport(models.Model):

    '''Required Fields'''
    pet_type = models.CharField(max_length=10, choices = PET_TYPE_CHOICES, null=False, default=None)
    status = models.CharField(max_length = 5, choices = STATUS_CHOICES, null=False, default=None)
    date_lost_or_found = models.DateField(null=False)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, null=False)
    size = models.CharField(max_length=30, choices = SIZE_CHOICES, null=False)
    location = models.CharField(max_length=25, null=False, default='unknown')

    #ForeignKey: Many-to-one relationship with User
    proposed_by = models.ForeignKey('UserProfile', null=False, default=None)

    '''Non-Required Fields'''
    img_path = models.ImageField(upload_to='images/petreport_images', null=True)
    pet_name = models.CharField(max_length=15, null=True, default='unknown') 
    age = models.CharField(max_length=10, null=True, default= 'unknown')
    color = models.CharField(max_length=30, null=True,default='unknown')
    breed = models.CharField(max_length=30, null=True,default='unknown')
    revision_number = models.IntegerField(null=True) #update revision using view
    description   = models.CharField(max_length=500, null=True, default="")
    #Many-to-Many relationship with User
    workers = models.ManyToManyField('UserProfile', null=True, related_name='workers_related')
    bookmarked_by = models.ManyToManyField('UserProfile', null=True, related_name='bookmarks_related')
    
    def save(self, *args, **kwargs):

        if self.id == None:
            print "%s has been saved!" % self
        else:
            print "%s has been updated!" % self

        super(PetReport, self).save(args, kwargs)            
        return self

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
        
#The User Profile Model containing a 1-1 association with the 
#django.contrib.auth.models.User object, among other attributes.
class UserProfile (models.Model):

    '''Required Fields'''
    user = models.OneToOneField(User, null=False, default=None)
    photo = models.ImageField(upload_to='images/profile_images', null=True)

    '''Non-Required Fields'''
    friends = models.ManyToManyField('self', null=True)
    chats = models.ManyToManyField('Chat', null=True)
    # facebook_cred = models.CharField(max_length=100, null=True)
    # twitter_cred = models.CharField(max_length=100, null=True)
    reputation = models.IntegerField(default=0, null=True)
    #facebook_id = models.IntegerField(blank=True, null=True)
    #twitter_id = models.IntegerField(blank=True, null=True)
    
    def __unicode__ (self):
        return '{ID{%s} %s}' % (self.id, self.user.username)

#The Pet Match Object Model
class PetMatch(models.Model):

    '''Required Fields'''
    lost_pet = models.ForeignKey('PetReport', null=False, default=None, related_name='lost_pet_related')
    found_pet = models.ForeignKey('PetReport', null=False, default=None, related_name='found_pet_related')
    proposed_by = models.ForeignKey('UserProfile', null=False, related_name='proposed_by_related')
    proposed_date = models.DateField(null=False, default=None, auto_now_add=True)
    description = models.CharField(max_length=300, null=False, default=None)
    
    '''Non-Required Fields'''
    is_open = models.BooleanField(default=True)
    score = models.IntegerField(default=0)
    closed_by = models.ForeignKey('UserProfile', null=True, related_name='closed_by_related')
    closed_date = models.DateField(null=True)
    up_votes = models.ManyToManyField('UserProfile', null=True, related_name='up_votes_related')
    down_votes = models.ManyToManyField('UserProfile', null=True, related_name='down_votes_related')

    '''Because of the Uniqueness constraint that the PetMatch must uphold, we override the save method'''
    def save(self, *args, **kwargs):
        #First, try to find an existing PetMatch
        lost_pet = self.lost_pet
        found_pet = self.found_pet
        
        #PetMatch inserted improperly
        if (lost_pet.status != "Lost") or (found_pet.status != "Found"):
            print "INSERTED IMPROPERLY"
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
        super(PetMatch, self).save(args, kwargs)
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
    text = models.CharField (max_length=10000, blank=True, null=False, default=None)
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
    location = forms.CharField(label = "Location", max_length = 50, required = True)

    '''Non-Required Fields'''
    img_path = forms.ImageField(label = "Upload an Image ", required = False)
    pet_name = forms.CharField(label = "Pet Name", max_length=50, required = False) 
    age = forms.CharField(label = "Age", max_length = 5, required = False)
    breed = forms.CharField(label = "Breed", max_length = 30, required = False)
    color = forms.CharField(label = "Coat Color(s)", max_length = 20, required = False)
    description  = forms.CharField(label = "Description", max_length = 500, required = False, widget = forms.Textarea)

    class Meta:
        model = PetReport
        exclude = ('revision_number', 'workers', 'proposed_by','bookmarked_by')



''' ============================ [SIGNALS] ==================================== '''

''' Create a post delete signal function to delete a UserProfile when a User/UserProfile is deleted'''
@receiver (pre_delete, sender=UserProfile)
def delete_UserProfile(sender, instance=None, **kwargs):
    #Remove the Log file associated with this UserProfile.
    log_path = ACTIVITY_LOG_DIRECTORY + str(instance.user.username) + ".log"
    if os.path.isfile(log_path):
        try:
            print "removing %s" % (log_path)
            os.unlink(log_path)
        except Exception, e:
            print e

    #Instead of deleting the User (which might break foreign-key relationships), let's set the active flag to False (INACTIVE)
    instance.user.is_active = False

''' Create a post save signal function to setup a UserProfile when a User is created'''
@receiver (post_save, sender=User)
def setup_UserProfile(sender, instance, created, **kwargs):
    if created == True:
        #Create a UserProfile object.
        UserProfile.objects.create(user=instance)
        #Create the first activity for this user
        log_activity(ACTIVITY_ACCOUNT_CREATED, instance.get_profile())




''' Import statements placed at the bottom of the page to prevent circular import dependence '''
from logging import log_activity