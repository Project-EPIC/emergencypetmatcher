from django.db import models

class PetReport(models.Model):

    #Required Fields
    pet_type = models.CharField(max_length=30,null=False)
    lost = models.BooleanField(null=False)
    #ForeignKey: One-to-Many relationship with User
    proposed_by = models.ForeignKey('User', null=False)

    #Non-Required Fields
    pet_name=models.CharField(max_length=30,null=True) 
    location = models.CharField(max_length=25,null=True)
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
    #proposed_matches = models.ForeignKey('PetMatch', null=True)

    #Many-to-Many relationship with User
    workers = models.ManyToManyField('User', null=True, related_name="workers")
    #One-to-One relationship with Chat
    chat = models.OneToOneField('Chat', null=True)
    #Many-to-One (Foreign Key) Relationship with User
    reports_submitted = models.ForeignKey('User', null=True, related_name = "reports_submitted")

    def __unicode__(self):
        return ' {type:%s, lost:%s, contact: %s}' % (self.pet_type, self.lost, self.proposed_by)


#The User Object Model.
class User (models.Model):

    #Required Fields
    username = models.CharField(max_length=100, null=False, default = None)
    password = models.CharField(max_length=100, null=False, default = None)
    first_name = models.CharField(max_length=100, null=False, default = None)
    last_name = models.CharField(max_length=100, null=False, default = None)
    email = models.EmailField(max_length=100, null=False, default = None)

    #Non-Required Fields
    facebook_cred = models.CharField(max_length=100, null=True)
    twitter_cred = models.CharField(max_length=100, null=True)
    reputation = models.IntegerField(default=0, null=True)
    #facebook_id = models.IntegerField(blank=True, null=True)
    #twitter_id = models.IntegerField(blank=True, null=True)

    friends = models.ManyToManyField('self', null=True)
    chats = models.ManyToManyField('Chat', null=True)


#The Chat Object Model
class Chat (models.Model):
    pass

    #Required Fields

    #Non-Required Fields

    #content has a List of DictFields of {User, text, date+time}. Note that the auto_now option means that
    #once a dictfield has been added or edited to this object instance, the date and time is recorded here.

    #ListField(DictField(EmbeddedModelField('User', null=False), 
     #   models.CharField(max_length=1000, blank=True), models.DateTimeField(auto_now_add=True)))

    #def __unicode__ (self):
    #    return ' {pet_report:%s}' % (self.pet_report)

#The Pet Match Object Model
class PetMatch(models.Model):

    #Required Fields
    lost_pet = models.OneToOneField('PetReport', null=False, related_name="lost_pet")
    found_pet = models.OneToOneField('PetReport', null=False, related_name="found_pet")
    proposed_by = models.OneToOneField('User', null=False, related_name="proposed_by")
    
    #Non-Required Fields
    proposed_date = models.DateTimeField(auto_now_add = True)
    is_open = models.BooleanField(default=True)
    score = models.IntegerField(default=0)
    closed_by = models.OneToOneField(User, null=True)
    closed_date = models.DateTimeField(null=True)
    up_votes = models.ManyToManyField('User', null=True, related_name="up_votes")
    down_votes = models.ManyToManyField('User', null=True, related_name="down_votes")
    matches_proposed = models.ForeignKey('User', null=True, related_name="matches_proposed")

    def __unicode__ (self):
        return ' {%s:%s}' % (self.lost_pet, self.found_pet)

