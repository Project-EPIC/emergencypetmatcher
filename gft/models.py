from django.db import models
from django import forms
# Create your models here.

class GFTEntry(forms.Form):
    pet_name = forms.CharField(max_length=50)
    contact = forms.CharField(max_length=50)
    tags = forms.CharField(max_length=150)
    latitude = forms.DecimalField(max_digits=15, decimal_places=9)
    longitude = forms.DecimalField(max_digits=15, decimal_places=9)
    lostfound = forms.BooleanField()
    photograph = forms.CharField(max_length=100)

