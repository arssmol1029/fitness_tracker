from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),  # Регистрация
    path('', views.dashboard, name='dashboard'),  # Главная страница
]