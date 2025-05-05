from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import forms
from django.contrib.auth.decorators import login_required
from .models import Workout, Exercise, WorkoutExercises, ExerciseSet
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.db.models import Q
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response


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
def workoutCreateView(request): 
    if request.method == 'POST':
        form = forms.WorkoutForm(request.POST)
        if form.is_valid():
            is_template_data = request.POST.get('is_template', 'false') == 'true'
            workout = form.save(commit=False)
            workout.user = request.user
            workout.is_template = is_template_data
            workout.save()

            exercises_data = json.loads(request.POST.get('exercises', '[]'))
            
            for ex in exercises_data:
                workout_exercise = WorkoutExercises.objects.create(
                    workout_id=workout.id,
                    exercise_id=ex['exercise_id'],
                )
                sets=ex['sets']
                number = 1
                for set in sets:
                    ExerciseSet.objects.create(
                        workout_exercise_id=workout_exercise.id,
                        set_number=number,
                        reps=set['reps'],
                        weight=set.get('weight'),
                    )
                    number += 1


            return JsonResponse({'status': 'ok'})
        
        return JsonResponse({'status': 'error', 'redirect_url': reverse('error_page')})
     
    else:
        form = forms.WorkoutForm()

    return render(request, 'tracker/workouts/workout.html', {'form': form})


@api_view(['GET'])
def exerciseSearch(request):
    term = request.data.get('term', '')
    exercises = Exercise.objects.filter((Q(is_custom=False) | Q(user=request.user)) & Q(name__icontains=term.capitalize()))
    results = [{'id': exercise.id, 'text': exercise.name, 'is_own_weight': exercise.is_own_weight} 
               for exercise in exercises]
    return Response({'results': results})



'''
def loadTemplate(request, workout_id):
    try:
        template = Workout.objects.get(id=workout_id, is_template=True)
        exercises = []
        for te in template.workoutexercises_set.all():
            exercises.append({
                'exercise_id': te.exercise.id,
                'name': te.exercise.name,
            })
        return JsonResponse({
            'status': 'ok',
            'title': template.title,
            'exercises': exercises
        })
    except Workout.DoesNotExist:
        path = reverse('error_page')
        return JsonResponse({
            'status': 'error',
            'code': 'not_exist',
            'message': 'шаблон не найден',
            'redirect_url': path,
        })
'''



@require_POST
def deleteTemplate(request, workout_id):
    if not request.user.is_authenticated:
        path = reverse('login')
        return JsonResponse({
            'status': 'error',
            'code': 'no_auth',
            'message': 'пользователь не авторизован',
            'redirect_url': path,
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
            'redirect_url': path,
        })
      


def errorPage(request):
    return render(request, 'tracker/error-page.html')
