from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.myLogin, name='login'),
    path('logout/', views.myLogout, name='logout'),

    path('', views.mainPage, name='main_page'),

    path('exercises/search/', views.exerciseSearch, name='exercise_search'),

    path('workouts/new/', views.workoutCreateView, name='workout_new'),
    path('workouts/edit/<int:pk>', views.workoutEditView, name='workout_edit'),
    path('workouts/day', views.dayView, name='workout_day'),
    path('workouts/template-delete/<int:workout_id>/', views.deleteTemplate, name='template_delete'),
]