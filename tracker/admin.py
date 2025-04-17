from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile, Workout, Exercise

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профили'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

admin.site.register(Workout)
admin.site.register(Exercise) 

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)