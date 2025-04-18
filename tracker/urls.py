from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),  # Регистрация
    path('', views.mainPage, name='main_page'),  # Главная страница
    path('new-exercise/', views.addCustomExercise, name='new_exercise'),
    path('new-workout/', views.newWorkout, name='new_workout'),
    path('workout/<int:workout_id>', views.editWorkout, name='edit_workout'),
]