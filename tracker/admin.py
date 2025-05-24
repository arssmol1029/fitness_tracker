from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from .models import Profile, Workout, Exercise, WorkoutExercise, ExerciseSet
import nested_admin

class ExerciseSetInline(nested_admin.NestedTabularInline):
    model = ExerciseSet
    extra = 1

class WorkoutExerciseInline(nested_admin.NestedTabularInline):
    model = WorkoutExercise
    extra = 1
    inlines = [ExerciseSetInline]

class WorkoutAdmin(nested_admin.NestedModelAdmin):
    model = Workout
    inlines = [WorkoutExerciseInline]

admin.site.register(Workout, WorkoutAdmin)
admin.site.register(Exercise)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Профили'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)