from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.db.models.signals import post_save
from django.core.files.storage import FileSystemStorage
import PIL

'''Enums for Various Model Choice Fields'''
PET_TYPE_CHOICES = [('Dog', 'Dog'), ('Cat', 'Cat'), ('Turtle', 'Turtle'), ('Rabbit', 'Rabbit'), ('Other', 'Other')]
STATUS_CHOICES = [('Lost','Lost'),('Found','Found')]
SEX_CHOICES=[('M','Male'),('F','Female')]
SIZE_CHOICES = [('L', 'Large (100+ lbs.)'), ('M', 'Medium (10 - 100 lbs.)'), ('S', 'Small (0 - 10 lbs.)')]
BREED_CHOICES = [('Scottish Terrier','Scottish Terrier'),('Golden Retriever','Golden Retriever'),('Yellow Labrador','Yellow Labrador')]

class PetReport(models.Model):

    '''Required Fields'''
    pet_type = models.CharField(max_length=10, choices = PET_TYPE_CHOICES, null=False, default=None)
    status = models.CharField(max_length = 5, choices = STATUS_CHOICES, null=False, default=None)
    date_lost_or_found = models.DateTimeField(auto_now_add=True, null=False)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, null=False)
    size = models.CharField(max_length=50, choices = SIZE_CHOICES, null=False)
    location = models.CharField(max_length=50, null=False, default='N/A')

    #ForeignKey: Many-to-one relationship with User
    proposed_by = models.ForeignKey('UserProfile', null=False, default=None)

    '''Non-Required Fields'''
    img_path = models.ImageField(upload_to='images/petreport_images', null=True)
    pet_name = models.CharField(max_length=50,null=True) 
    age = models.IntegerField(null=True)
    color = models.CharField(max_length=20,null=True)
    breed = models.CharField(max_length=30,null=True)
    revision_number = models.IntegerField(null=True) #update revision using view
    description   = models.CharField(max_length=300, null=True)
    #Many-to-Many relationship with User
    workers = models.ManyToManyField('UserProfile', null=True, related_name='workers_related')

    def __unicode__(self):
        return 'PetReport {pet_type: %s, status: %s, proposed_by: %s}' % (self.pet_type, self.status, self.proposed_by)

    def long_unicode (self):
        str = "PetReport {\n\tpet_type: %s\n\tstatus: %s\n\tproposed_by: %s\n\t" % (self.pet_type, self.status, self.proposed_by)
        str += "date_lost_or_found: %s\n\tsex: %s\n\tsize: %s\n\tlocation: %s\n\t" % (self.date_lost_or_found, self.sex, self.size, self.location)
        str += "age: %s\n\tbreed: %s\n\tdescription: %s\n\t}" % (self.age, self.breed, self.description)
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

    ''' Create a post save signal function to save a UserProfile when a User is created'''
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)

    def __unicode__ (self):
        return 'User {username:%s, email:%s}' % (self.user.username, self.user.email)


#The Pet Match Object Model
class PetMatch(models.Model):

    '''Required Fields'''
    lost_pet = models.OneToOneField('PetReport', null=False, related_name='lost_pet_related')
    found_pet = models.OneToOneField('PetReport', null=False, related_name='found_pet_related')
    proposed_by = models.ForeignKey('UserProfile', null=False, related_name='proposed_by_related')
    
    '''Non-Required Fields'''
    proposed_date = models.DateTimeField(auto_now_add = True)
    is_open = models.BooleanField(default=True)
    score = models.IntegerField(default=0)
    closed_by = models.ForeignKey('UserProfile', null=True, related_name='closed_by_related')
    closed_date = models.DateTimeField(null=True)
    up_votes = models.ManyToManyField('UserProfile', null=True, related_name='up_votes_related')
    down_votes = models.ManyToManyField('UserProfile', null=True, related_name='down_votes_related')
    matches_proposed = models.ForeignKey('UserProfile', null=True, related_name='matches_proposed_related')

    def __unicode__ (self):
        return 'PetMatch {lost:%s, found:%s, proposed_by:%s}' % (self.lost_pet, self.found_pet, self.proposed_by)

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


''' Form Models - These Models nicely organize the model-related data into Django Form objects that have built-in validation
functionality and can be passed around via POST requests. Order of Fields matter.'''

#The PetReport ModelForm
class PetReportForm (ModelForm):

    '''Required Fields'''
    pet_type = forms.ChoiceField(label = 'Pet Type', choices = PET_TYPE_CHOICES, required = True)
    status = forms.ChoiceField(label = "Status (Lost/Found)", choices = STATUS_CHOICES, required = True)
    date_lost_or_found = forms.DateTimeField(label = "Date Lost/Found", required = True)
    sex = forms.ChoiceField(label = "Sex", choices = SEX_CHOICES, required = True)
    size = forms.ChoiceField(label = "Size of Pet", choices = SIZE_CHOICES, required = True)
    location = forms.CharField(label = "Location", max_length = 50, required = True)

    '''Non-Required Fields'''
    img_path = forms.ImageField(label = "Upload an Image ", required = False)
    pet_name = forms.CharField(label = "Pet Name", max_length=50, required = False) 
    age = forms.IntegerField(label = "Age", required = False)
    breed = forms.CharField(label = "Breed", max_length = 30, required = False)
    color = forms.CharField(label = "Coat Color(s)", max_length = 20, required = False)
    description  = forms.CharField(label = "Description", max_length = 300, required = False, widget = forms.Textarea)

    class Meta:
        model = PetReport
        exclude = ('revision_number', 'workers', 'proposed_by')










