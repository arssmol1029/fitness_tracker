from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import forms
from django.contrib.auth.decorators import login_required
from .models import Workout
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse

@login_required
def mainPage(request):
    global_workouts = Workout.objects.filter(is_custom = False)
    custom_workouts = Workout.objects.filter(is_custom = True, user = request.user)

    return render(
        request,
        'tracker/main-page.html',   
        {
            'global_workouts': global_workouts,
            'custom_workouts': custom_workouts,
        },
    )

def signup(request):
    if request.user.is_authenticated:
        return redirect('main_page')

    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main_page')
    else:
        form = forms.SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})

def myLogin(request):
    if request.user.is_authenticated:
        next_url = request.GET.get('next', 'main_page')
        return redirect(next_url)
    
    if request.method == 'POST':
        form = forms.LoginForm(request, data=request.POST)
        if form.is_valid():
            user=form.get_user()

            login(request, user)
            next_url = request.GET.get('next', 'main_page')
            return redirect(next_url)
    else:
        form = forms.LoginForm()

    return render(request, 'registration/login.html', {'form': form})

def myLogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')

@login_required
def addCustomExercise(request):
    if request.method == 'POST':
        form = forms.ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(False)
            exercise.user = request.user
            exercise.is_custom = True
            exercise.save()
            return redirect('main_page')
    else:
        form = forms.ExerciseForm()
    
    return render(request, 'tracker/exercises/new-custom-exercise.html', {'form': form})
    
@login_required
def addWorkoutTemplate(request):
    if request.method == 'POST':
        form = forms.WorkoutForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('main_page')
    else:
        form = forms.WorkoutForm(user=request.user)

    return render(request, 'tracker/workouts/templates/new-template.html', {'form': form})

@login_required
def editTemplate(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id)

    return render(request, 'tracker/workouts/templates/edit-template.html', {'workout': workout})

@require_POST
def deleteTemplate(request, workout_id):
    if not request.user.is_authenticated:
        path = reverse('login')
        return JsonResponse({
            'status': 'error',
            'code': 'no_auth',
            'message': 'пользователь не авторизован',
            'redirect': path,
        })
    try:
        workout = Workout.objects.get(id=workout_id)
        workout.delete()
        return JsonResponse({'status': 'ok'})
    except Workout.DoesNotExist:
        path = reverse('error_page')
        return JsonResponse({
            'status': 'error',
            'code': 'no_workout',
            'message': 'объект не найден',
            'redirect': path,
        })
    
def errorPage(request):
    return render(request, 'tracker/error-page.html')
