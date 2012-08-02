from django.contrib import admin
from home.models import *

class PetReportAdmin(admin.ModelAdmin):

    fieldsets = [
        (None, {
            'fields': ('pet_type', 'status', 'date_lost_or_found','proposed_by','sex','size','location','pet_name','age','color','breed','description','workers')
        })
    ]
    
    list_display = ('pet_type', 'status', 'date_lost_or_found','proposed_by','sex','size','location','pet_name','age','color','breed') 

class PetMatchAdmin(admin.ModelAdmin):   
    list_display = ('lost_pet','found_pet','proposed_by','proposed_date','score','closed_by','closed_date','matches_proposed')

class UserProfileInline(admin.StackedInline):
	model = UserProfile

class UserAdmin(admin.ModelAdmin):   
	inlines = [
		UserProfileInline,
	]

admin.site.register(PetReport,PetReportAdmin)
admin.site.register(UserProfile)
admin.site.register(PetMatch,PetMatchAdmin)
admin.site.unregister(User)
admin.site.register(User,UserAdmin)
