from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),  # Регистрация
    path('', views.dashboard, name='dashboard'),  # Главная страница
    path('new-exercise/', views.addCustomExercise, name='new_exercise'),
    path('new_workout/', views.newWorkout, name='new_workout'),
]