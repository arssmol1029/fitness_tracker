from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.myLogin, name='login'),
    path('logout', views.myLogout, name='logout'),

    path('', views.mainPage, name='main_page'),

    path('profile', views.profilePage, name='profile_page'),

    path('exercises/search', views.exerciseSearch, name='exercise_search'),
    path('exercises/create', views.exerciseCreate, name='exercise_create'),
    path('exercises/list', views.exerciseListView, name='exercise_list'),
    path('exercises/delete/<int:pk>', views.exerciseDelete, name='exercise_delete'),

    path('workouts/templates/search', views.templateSearch, name='template_search'),
    path('workouts/templates/<int:pk>', views.templateLoad, name='template_load'),

    path('workouts', views.workoutListView, name='workout_list'),
    path('workouts/create', views.workoutCreateView, name='workout_create'),
    path('workouts/edit/<int:pk>', views.workoutEditView, name='workout_edit'),
    path('workouts/day', views.workoutDayListView, name='workout_day_list'),
    path('workouts/delete/<int:pk>', views.workoutDelete, name='workout_delete'),
]