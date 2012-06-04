from django.db import models
from djangotoolbox.fields import ListField, EmbeddedModelField
from django_mongodb_engine.contrib import MongoDBManager

# Create your models here.
class Pets(models.Model):
    class Meta:
        db_table = "pets_alpha"

    revisions = models.IntegerField()
    entries = ListField(EmbeddedModelField('PetReport'))
    match = EmbeddedModelField('PetReport', null=True)

class PetReport(models.Model):
    pet_type = models.CharField()
    img = models.CharField()
    img_useful = models.BooleanField()
    lost = models.BooleanField()
    author = models.CharField()
    color = models.CharField()
    age = models.CharField()
    breed = models.CharField()
    comments = models.CharField()
    sex = models.CharField()
    date = models.DateTimeField()
    size = models.CharField()
    revision = models.IntegerField()
    upvotes = ListField()

    objects = MongoDBManager()
