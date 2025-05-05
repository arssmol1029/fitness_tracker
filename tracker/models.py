from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True, help_text="Рост в см")
    weight = models.FloatField(null=True, blank=True, help_text="Вес в кг")

    def __str__(self):
        return f"Профиль {self.user.username}"

   
class Exercise(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100)
    is_custom = models.BooleanField(default=True)
    is_own_weight = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Workout(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=100, default='тренировка')
    date = models.DateField(null=True, blank=True)
    is_template = models.BooleanField(default=False)
    is_custom = models.BooleanField(default=True)
    exercises = models.ManyToManyField(
        Exercise,
        blank=True,
        through='tracker.WorkoutExercises',
        through_fields=('workout', 'exercise'),
    )

    def __str__(self):
        return self.name

class WorkoutExercises(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)

class ExerciseSet(models.Model):
    workout_exercise = models.ForeignKey(
        WorkoutExercises,
        on_delete=models.CASCADE,
        related_name='exercise_sets',
    )
    set_number = models.PositiveIntegerField(default=1)
    reps = models.PositiveIntegerField()
    weight = models.FloatField(null=True, blank=True)

# Cоздание профиля при регистрации
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()