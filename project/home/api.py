# home/api.py
from tastypie.authorization import Authorization
from tastypie.authentication import BasicAuthentication
from tastypie.authorization import DjangoAuthorization
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from tastypie.serializers import Serializer
from tastypie.exceptions import *
from home.models import UserProfile, PetReport
from django.db import IntegrityError
from datetime import datetime
from utils import *
from logging import *

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'auth/user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        # fields = ['username', 'first_name', 'last_name', 'last_login']
        allowed_methods = ['get', 'post', 'put']
        authentication = BasicAuthentication()
        authorization = DjangoAuthorization()
        # serializer = Serializer()
        # always_return_data=True


class UserProfileResource(ModelResource):
    # proposed_related = fields.ToManyField('home.api.UserProfileResource', 'proposed_by', full=True)
    user = fields.ForeignKey(UserResource, 'user', full=True) 

    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'userprofile'
        # include_resource_uri = False

    # def dehydrate(self, bundle):
    #     return bundle.data['first_name']

from django.core.exceptions import ValidationError

class PetReportResource(ModelResource):
    proposed_by = fields.ForeignKey(UserProfileResource, 'proposed_by', full=True)

    class Meta:
        queryset = PetReport.objects.all()
        resource_name = 'petreport'
        # include_resource_uri = False
        allowed_methods = ['get', 'post']

        authentication = BasicAuthentication()
        authorization = Authorization()
        always_return_data=True

    def obj_create(self, bundle, request=None, **kwargs):
        
        try: 
            form = PetReportForm(bundle.data)

            if form.is_valid() == True:
                pr = form.save(commit=False)
                #Create (but do not save) the Pet Report Object associated with this form data.
                pr.proposed_by = request.user.get_profile()
                print "[INFO]: Pet Report Image Path: %s" % pr.img_path
                #If there was no image attached, let's take care of defaults.
                if pr.img_path == None:
                    if pr.pet_type == PETREPORT_PET_TYPE_DOG:
                        pr.img_path.name = "images/defaults/dog_silhouette.jpg"
                    elif pr.pet_type == PETREPORT_PET_TYPE_CAT:
                        pr.img_path.name = "images/defaults/cat_silhouette.jpg"
                    elif pr.pet_type == PETREPORT_PET_TYPE_BIRD:
                        pr.img_path.name = "images/defaults/bird_silhouette.jpg"                    
                    elif pr.pet_type == PETREPORT_PET_TYPE_HORSE:
                        pr.img_path.name = "images/defaults/horse_silhouette.jpg"
                    elif pr.pet_type == PETREPORT_PET_TYPE_RABBIT:
                        pr.img_path.name = "images/defaults/rabbit_silhouette.jpg"
                    elif pr.pet_type == PETREPORT_PET_TYPE_SNAKE:
                        pr.img_path.name = "images/defaults/snake_silhouette.jpg"                                       
                    elif pr.pet_type == PETREPORT_PET_TYPE_TURTLE:
                        pr.img_path.name = "images/defaults/turtle_silhouette.jpg"
                    else:
                        pr.img_path.name = "images/defaults/other_silhouette.jpg"
        
                #Now save the Pet Report.        
                pr.save() 
                if pr.status == 'Lost':
                    bundle.data ['message'] = 'Thank you for your submission! Your contribution will go a long way towards helping people find your lost pet.'
                else:
                    bundle.data ['message'] = 'Thank you for your submission! Your contribution will go a long way towards helping others match lost and found pets.'

                #Log the PetReport submission for this UserProfile
                log_activity(ACTIVITY_PETREPORT_SUBMITTED, request.user.get_profile(), petreport=pr)
                print "[SUCCESS]: Pet Report submitted successfully" 
                bundle.obj = pr #model_to_dict(pr)

        except Exception as e:
            raise BadRequest(e)

        return bundle





  

 
