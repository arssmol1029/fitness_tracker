from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.myLogin, name='login'),
    path('logout/', views.myLogout, name='logout'),

    path('', views.mainPage, name='main_page'),

    path('exercise/new/', views.addCustomExercise, name='new_exercise'),

    path('workout/new-template/', views.addWorkoutTemplate, name='new_template'),
    path('workout/<int:workout_id>/edit-template/', views.editTemplate, name='edit_template'),
    path('workout/<int:workout_id>/delete-template/', views.deleteTemplate, name='delete_template'),

    path('error404/', views.errorPage, name='error_page'),
]