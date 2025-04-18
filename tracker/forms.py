from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Workout, Exercise

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        label='Email',
        required=True,
    )

    birth_date = forms.DateField(
        label='Дата рождения',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'}),
    )
    
    height = forms.FloatField(
        label='Рост (см)',
        required=False,
        min_value=50,
        max_value=250 
    )
    
    weight = forms.FloatField(
        label='Вес (кг)',
        required=False,
        min_value=20,
        max_value=300
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'birth_date',
            'height',
            'weight'
        )

    '''
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():  # Проверяем, не занят ли email
            raise forms.ValidationError("Этот email уже используется.")
        return email
    '''

    def save(self, commit = True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.save()
        
        if commit:
            profile = user.profile
            profile.birth_date = self.cleaned_data['birth_date']
            profile.height = self.cleaned_data['height']
            profile.weight = self.cleaned_data['weight']
            profile.save()
        return user
    
class ExerciseForm(forms.ModelForm):
    name = forms.CharField(
        label='Название',
        max_length=100,
    )

    class Meta:
        model = Exercise
        fields = (
            'name',
        )

    def save(self, commit = True):
        exercise = super().save(commit=False)
        exercise.name = self.cleaned_data['name'].capitalize()
        if commit:
            exercise.save()
        return exercise
    
class WorkoutForm(forms.ModelForm):
    name = forms.CharField(
        label='Название',
        max_length=100,
    )

    global_exercises = forms.ModelMultipleChoiceField(
        queryset=Exercise.objects.filter(is_custom=False),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    custom_exercises = forms.ModelMultipleChoiceField(
        queryset=Exercise.objects.filter(is_custom=True),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Workout
        fields = (
            'name',
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if not self.user or not self.user.is_authenticated:
            del self.fields['custom_exercises']
        else:
            self.fields['custom_exercises'].queryset = Exercise.objects.filter(is_custom=True, user = self.user)
    
    def save(self, commit = True):
        workout = super().save(commit=False)
        workout.name = self.cleaned_data['name'].capitalize()
        workout.is_custom = True
        if self.user:
            workout.user = self.user

        if commit:
            workout.save()
        
        all_exercises = list(self.cleaned_data['global_exercises']) + list(self.cleaned_data['custom_exercises'])
        workout.exercises.set(all_exercises)

        return workout
