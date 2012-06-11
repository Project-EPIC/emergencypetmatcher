from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField, DictField
from django_mongodb_engine.contrib import MongoDBManager

class PetReport(models.Model):

    #Required Fields
    pet_type = models.CharField(max_length=30,null=False)
    lost = models.BooleanField(null=False)
    proposed_by = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=25,null=False)

    #Non-Required Fields
    pet_name=models.CharField(max_length=30,null=True) 
    color = models.CharField(max_length=20,null=True)
    age = models.IntegerField(null=True)
    breed = models.CharField(max_length=30,null=True)
    size = models.CharField(max_length=30, null=True)
    description   = models.CharField(max_length=300,null=True)
    revision_number = models.IntegerField(null=True) #update revision using view
    SEX_CHOICES=(
        ('Male','Male'),
        ('Female','Female')
        )
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)
    date_lost_or_found = models.DateTimeField(auto_now_add=True)
    proposed_matches = ListField(EmbeddedModelField('PetMatch', null=True))
    workers = ListField(EmbeddedModelField('User', null=True))
    chat = EmbeddedModelField('Chat', null=True)

    def __unicode__(self):
        return 'PetReport{%s, lost:%s contact: %s}' % (self.pet_type, self.lost, self.proposed_by)


#The User Object Model.
class User (models.Model):

    #Required Fields
    username = models.CharField(max_length=100, null=False)
    password = models.CharField(max_length=100, null=False)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    email = models.EmailField(max_length=100, null=False)

    #Non-Required Fields
    facebook_cred = models.CharField(max_length=100, null=True)
    twitter_cred = models.CharField(max_length=100, null=True)
    reputation = models.IntegerField(default=0, null=True)
    #facebook_id = models.IntegerField(blank=True, null=True)
    #twitter_id = models.IntegerField(blank=True, null=True)
    friends = ListField(EmbeddedModelField('User', null=True))
    chats = ListField(EmbeddedModelField('Chat', null=True))
    reports_working_on = ListField(EmbeddedModelField('PetReport', null=True))
    reports_submitted = ListField(EmbeddedModelField('PetReport', null=True))
    matches_proposed = ListField(EmbeddedModelField('PetMatch', null=True))
    
    #fr = ListField(models.CharField(max_length=100))
    


#The Chat Object Model
class Chat (models.Model):

    #Required Fields
    pet_report = EmbeddedModelField('PetReport', null=False)

    #Non-Required Fields
    current_users = ListField(EmbeddedModelField('User', null=True))
    #content has a List of DictFields of {User, text, date+time}. Note that the auto_now option means that
    #once a dictfield has been added or edited to this object instance, the date and time is recorded here.
    content = ListField(DictField(EmbeddedModelField('User', null=False), 
        models.CharField(max_length=1000, blank=True), models.DateTimeField(auto_now_add=True)))

    def __unicode__ (self):
        return 'Chat {pet_report:%s}' % (self.pet_report)


#The Pet Match Object Model
class PetMatch(models.Model):

    #Required Fields
    lost_pet = EmbeddedModelField('PetReport', null=False)
    found_pet = EmbeddedModelField('PetReport', null=False)
    proposed_by = EmbeddedModelField('User', null=False)
    
    #Non-Required Fields
    proposed_date = models.DateTimeField(auto_now_add = True)
    is_open = models.BooleanField(default=True)
    score = models.IntegerField(default=0)
    closed_by = EmbeddedModelField(User, null=True)
    closed_date = models.DateTimeField(null=True)
    up_votes = ListField(EmbeddedModelField('User', null=True))
    down_votes = ListField(EmbeddedModelField('User', null=True))

    def __unicode__ (self):
        return 'PetMatch {%s:%s}' % (self.lost_pet, self.found_pet)

