from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.myLogin, name='login'),
    path('logout/', views.myLogout, name='logout'),

    path('', views.mainPage, name='main_page'),

    path('exercise/search/', views.exerciseSearch, name='exercise_search'),

    path('workouts/new-workout/', views.workoutCreateView, name='workout_new'),
    path('workouts/template-delete/<int:workout_id>/', views.deleteTemplate, name='template_delete'),

    path('error404/', views.errorPage, name='error_page'),
]