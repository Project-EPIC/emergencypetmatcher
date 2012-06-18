from django.db import models
from django.contrib.auth.models import User

class PetReport(models.Model):

    SEX_CHOICES=(('Male','Male'),('Female','Female'))
    PET_TYPES = (('Dog', 'Dog'), ('Cat', 'Cat'), ('Other', 'Other'))

    '''Required Fields'''
    pet_type = models.CharField(max_length=10, choices = PET_TYPES, null=False, default=None)
    lost = models.BooleanField(null=False, default=None)
    #ForeignKey: Many-to-one relationship with User
    proposed_by = models.ForeignKey('UserProfile', null=False, default=None)

    '''Non-Required Fields'''
    pet_name = models.CharField(max_length=50,null=True) 
    description   = models.CharField(max_length=300,null=True)
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)
    location = models.CharField(max_length=50,null=True)
    color = models.CharField(max_length=20,null=True)
    breed = models.CharField(max_length=30,null=True)
    size = models.CharField(max_length=30, null=True)
    age = models.IntegerField(null=True)
    revision_number = models.IntegerField(null=True) #update revision using view
    date_lost_or_found = models.DateTimeField(auto_now_add=True)
    #Many-to-Many relationship with User
    workers = models.ManyToManyField('UserProfile', null=True, related_name='%(app_label)s_%(class)s_workers_related')

    def __unicode__(self):
        return ' PetReport {pet_type:%s, lost:%s, contact: %s}' % (self.pet_type, self.lost, self.proposed_by)


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

    def __unicode__ (self):
        return ' User {username:%s, first_name:%s, last_name:%s, email:%s}' % (self.user.username, self.user.first_name, self.user.last_name, self.user.email)


#The Pet Match Object Model
class PetMatch(models.Model):

    '''Required Fields'''
    lost_pet = models.OneToOneField('PetReport', null=False, related_name='%(app_label)s_%(class)s_lost_pet_related')
    found_pet = models.OneToOneField('PetReport', null=False, related_name='%(app_label)s_%(class)s_found_pet_related')
    proposed_by = models.OneToOneField('UserProfile', null=False, related_name='%(app_label)s_%(class)s_proposed_by_related')
    
    '''Non-Required Fields'''
    proposed_date = models.DateTimeField(auto_now_add = True)
    is_open = models.BooleanField(default=True)
    score = models.IntegerField(default=0)
    closed_by = models.OneToOneField(User, null=True)
    closed_date = models.DateTimeField(null=True)
    up_votes = models.ManyToManyField('UserProfile', null=True, related_name='%(app_label)s_%(class)s_up_votes_related')
    down_votes = models.ManyToManyField('UserProfile', null=True, related_name='%(app_label)s_%(class)s_down_votes_related')
    matches_proposed = models.ForeignKey('UserProfile', null=True)

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

