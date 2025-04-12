from django import forms  # Базовый класс для форм
from django.contrib.auth.forms import UserCreationForm  # Стандартная форма регистрации
from django.contrib.auth.models import User  # Модель пользователя Django
from .models import Profile, Workout, Exercise # Наша модель профиля

class SignUpForm(UserCreationForm):
    # Добавляем поле email (обязательное)
    email = forms.EmailField(
        label='Email',
        required=True,  # Обязательное поле
        help_text='Введите действующий email'  # Подсказка под полем
    )

    # Добавляем дополнительные поля (необязательные)
    birth_date = forms.DateField(
        label='Дата рождения',
        required=False,  # Можно оставить пустым
        widget=forms.DateInput(attrs={'type': 'date'}),  # Календарь в HTML5
        help_text='Формат: ММ-ДД-ГГГГ'
    )
    
    height = forms.FloatField(
        label='Рост (см)',
        required=False,
        min_value=50,  # Минимальный рост
        max_value=250  # Максимальный рост
    )
    
    weight = forms.FloatField(
        label='Вес (кг)',
        required=False,
        min_value=20,
        max_value=300
    )

    class Meta:
        model = User  # Указываем, что форма работает с моделью User
        fields = (
            'username',  # Стандартное поле
            'email',     # Добавленное поле
            'password1', # Пароль (первое введение)
            'password2', # Подтверждение пароля
            'birth_date', # Наши кастомные поля
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
        # Сохраняем пользователя (родительский метод)
        user = super().save(commit=False)  # Не сохраняем сразу в БД
        user.email = self.cleaned_data.get('email')  # Присваиваем email
        user.save()  # Сохраняем пользователя в БД
        
        # Создаём профиль и заполняем данные
        if commit:
            profile = user.profile  # Профиль создаётся через сигнал
            profile.birth_date = self.cleaned_data['birth_date']
            profile.height = self.cleaned_data['height']
            profile.weight = self.cleaned_data['weight']
            profile.save()
        return user  # Возвращаем созданного пользователя
    
class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = (
            'name'
        )

    def save(self):
        exercise = super().save(commit=False)
        exercise.name = self.cleaned_data['name'].capitalize()
        exercise.save()
        return exercise
    
class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = (
            'name',
            'date',
            'exercises'
        )
    
    def save(self, commit = True):
        workout = super().save(commit=False)
        workout.name = self.cleaned_data['name'].capitalize()
        workout.date = self.cleaned_data['date']

        if commit:
            workout.save()
            self.save_m2m() 

        return workout
