from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
# from social_auth.models import Nonce
from django.contrib.auth.models import User
from socializing.models import UserProfile
from reporting.models import PetReport
from matching.models import PetMatch

class PetReportAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {
            'fields': ('pet_type', 'status', 'date_lost_or_found','proposed_by','sex','size','location','pet_name','age','color','breed','description','workers')
        })
    ]
    
    list_display = ('id','pet_type', 'status', 'date_lost_or_found','proposed_by','sex','size','location','pet_name','age','color','breed') 

class PetMatchAdmin(admin.ModelAdmin):   
    list_display = ('id','lost_pet','found_pet','proposed_by','proposed_date','is_successful')

class UserProfileInline(admin.StackedInline):
	model = UserProfile

class UserAdmin(admin.ModelAdmin):   
	inlines = [
		UserProfileInline,
	]
	list_display = ('id','username','first_name','last_name','email','is_staff','is_superuser','is_active')

class UserProfileAdmin(admin.ModelAdmin):
	list_display = ('id','user','reputation')	

admin.site.register(PetReport,PetReportAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(PetMatch,PetMatchAdmin)
admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.unregister(Site)
admin.site.unregister(Group)
