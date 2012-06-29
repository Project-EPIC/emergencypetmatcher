from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from django.db.models.signals import post_save

'''Enums for Various Model Choice Fields'''
PET_TYPE_CHOICES = [(None, 'Select'), ('Dog', 'Dog'), ('Cat', 'Cat'), ('Other', 'Other')]
STATUS_CHOICES = [(None, 'Select'),('Lost','Lost'),('Found','Found')]
SEX_CHOICES=[(None, 'Select'), ('M','Male'),('F','Female')]
SIZE_CHOICES = [(None, 'Select'), ('L', 'Large (100+ lbs.)'), ('M', 'Medium (10 - 100 lbs.)'), ('S', 'Small (0 - 10 lbs.)')]
BREED_CHOICES = [('Scottish Terrier','Scottish Terrier'),('Golden Retriever','Golden Retriever'),('Yellow Labrador','Yellow Labrador')]

class PetReport(models.Model):

    '''Required Fields'''
    pet_type = models.CharField(max_length=10, choices = PET_TYPE_CHOICES, null=False, default=None)
    status = models.CharField(max_length = 5, choices = STATUS_CHOICES, null=False, default=None)
    date_lost_or_found = models.DateTimeField(auto_now_add=True, null=False)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, null=False, default=None)
    size = models.CharField(max_length=50, choices = SIZE_CHOICES, null=False, default=None)
    location = models.CharField(max_length=50, null=False, default=None)

    #ForeignKey: Many-to-one relationship with User
    proposed_by = models.ForeignKey('UserProfile', null=False, default=None)

    '''Non-Required Fields'''
    pet_name = models.CharField(max_length=50,null=True) 
    age = models.IntegerField(null=True)
    color = models.CharField(max_length=20,null=True)
    breed = models.CharField(max_length=30,null=True)
    revision_number = models.IntegerField(null=True) #update revision using view
    img_path=models.CharField(max_length=100,null=True)
    description   = models.CharField(max_length=300, null=True)
    #Many-to-Many relationship with User
    workers = models.ManyToManyField('UserProfile', null=True, related_name='workers_related')


    def __unicode__(self):
        return ' PetReport {pet_type:%s, status:%s, contact: %s}' % (self.pet_type, self.status, self.proposed_by)


#The User Profile Model containing a 1-1 association with the 
#django.contrib.auth.models.User object, among other attributes.
class UserProfile (models.Model):

    '''Required Fields'''
    user = models.OneToOneField(User, null=False, default=None)

    '''Non-Required Fields'''
    friends = models.ManyToManyField('self', null=True)
    chats = models.ManyToManyField('Chat', null=True)
    facebook_cred = models.CharField(max_length=100, null=True)
    twitter_cred = models.CharField(max_length=100, null=True)
    reputation = models.IntegerField(default=0, null=True)
    #facebook_id = models.IntegerField(blank=True, null=True)
    #twitter_id = models.IntegerField(blank=True, null=True)

    ''' Create a post save signal function to save a UserProfile when a User is created'''
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    post_save.connect(create_user_profile, sender=User)

    def __unicode__ (self):
        return ' User {username:%s, first_name:%s, last_name:%s, email:%s}' % (self.user.username, self.user.first_name, self.user.last_name, self.user.email)


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
        return ' PetMatch {lost:%s, found:%s, proposed_by:%s}' % (self.lost_pet, self.found_pet, self.proposed_by)

#The Chat Object Model
class Chat (models.Model):

    '''Required Fields'''
    #One-to-One relationship with PetReport
    pet_report = models.OneToOneField('PetReport', null=False, default=None)

    def __unicode__ (self):
        return ' Chat {pet_report:%s}' % (self.pet_report)


#The Chat Line Object Model
class ChatLine (models.Model):

    '''Required Fields'''
    chat = models.ForeignKey('Chat', null=False, default=None)
    userprofile = models.ForeignKey('UserProfile', null=False, default=None)
    text = models.CharField (max_length=10000, blank=True, null=False, default=None)
    date = models.DateTimeField(auto_now_add=True)


''' Form Models - These Models nicely organize the model-related data into Django Form objects that have built-in validation
functionality and can be passed around via POST requests. Order of Fields matter.'''

#The PetReport ModelForm
class PetReportForm (ModelForm):

    '''Required Fields'''
    pet_type = forms.ChoiceField(label = 'Pet Type', choices = PET_TYPE_CHOICES, required = True)
    status = forms.ChoiceField(label = "Lost/Found", choices = STATUS_CHOICES, required = True)
    date_lost_or_found = forms.DateTimeField(label = "Date Lost/Found", required = True)
    sex = forms.ChoiceField(label = "Sex", choices=SEX_CHOICES, required = True)
    size = forms.ChoiceField(label = "Size of Pet", choices = SIZE_CHOICES, required = True)
    location = forms.CharField(label = "Location", max_length=50, required = True)

    '''Non-Required Fields'''
    pet_name = forms.CharField(label = "Pet Name", max_length=50, required = False) 
    age = forms.IntegerField(label = "Age", required = False)
    breed = forms.CharField(label = "Breed", max_length=30, required = False)
    color = forms.CharField(label = "Coat Color(s)", max_length=20, required = False)
    description  = forms.CharField(label = "Description", max_length=300, required = False, widget=forms.Textarea)

    class Meta:
        model = PetReport
        exclude = ("proposed_by", "workers", "revision_number")

    def __init__(self, *args, **kwargs):
        super(PetReportForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [ 'pet_type','status', 'date_lost_or_found', 'pet_name', 
        'sex', 'age', 'breed', 'size', 'color', 'location', 'description']


#The UserProfile ModelForm
class UserForm (ModelForm):
    #first_name = forms.CharField(label = "First Name", required = False)
    #last_name = forms.CharField(label = "Last Name", required = False)
    password_again = forms.CharField(label = "Password (again)", required = True, widget = forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'password_again')
        widgets = {
            'password': forms.PasswordInput()
        }




