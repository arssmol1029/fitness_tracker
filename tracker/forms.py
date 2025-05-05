from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from .models import Profile, Workout, Exercise, ExerciseSet
from django.db.models import Q
from datetime import date

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        error_messages={
            'required': 'Введите имя пользователя'
        },
    )

    email = forms.EmailField(
        label='Email',
        required=True,
        error_messages={
            'required': 'Введите email'
        },
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Введите пароль'
        },
    )

    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Введите пароль ещё раз'
        },
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'email',
            'password1',
            'password2',
            Submit('submit', 'Регистрация', css_class='btn-primary w-100'),
            HTML('<p class="text-center mt-3">Уже есть аккаунт? <a href="{% url \'login\' %}">Войти</a></p>'),
        )

    '''
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():  # Проверяем, не занят ли email
            raise forms.ValidationError("Этот email уже используется.")
        return email
    '''

    def save(self):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.save()
        
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        error_messages={
            'required': 'Введите имя пользователя'
        },
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': 'Введите пароль'
        },
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'username',
            'password',
            Submit('submit', 'Войти', css_class='btn-primary w-100'),
            HTML('<p class="text-center mt-3">Нет аккаунта? <a href="{% url \'signup\' %}">Зарегистрируйтесь</a></p>'),
        )

    error_messages = {
        'invalid_login': "Неверный логин или пароль",
    }
    
class WorkoutForm(forms.ModelForm):
    name = forms.CharField(
        label='Название',
        max_length=100,
    )

    date = forms.DateField(
        label='Дата',
        widget=forms.DateInput(attrs={'type': 'date'}),  # Активирует HTML5-календарь
        initial=date.today(),
    )

    class Meta:
        model = Workout
        fields = (
            'name',
            'date'
        )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
    
    def save(self, commit = True, is_template = False):
        workout = super().save(commit=False)
        workout.name = self.cleaned_data['name'].capitalize()
        workout.date = self.cleaned_data['date']

        if commit:
            workout.save()

        return workout


class SetForm(forms.ModelForm):
    reps = forms.IntegerField(min_value=1, max_value=120)
    weight = forms.DecimalField(decimal_places=3)
    class Meta:
        model = ExerciseSet
        fields = (
            'reps',
            'weight'
        )

    def __init__(self, *args, is_own_weight=False, **kwargs):
        super().__init__(*args, **kwargs)
        if is_own_weight:
            self.fields['weight'].disabled = True
        self.helper = FormHelper()

    def save(self, commit=True, is_own_weight=False):
        exercise_set = super.save(commit=False)
        exercise_set.reps = self.cleaned_data['reps']
        if not is_own_weight: 
            exercise_set.weight = self.cleaned_data['weight']

        if commit:
            exercise_set.save()

        return exercise_set
