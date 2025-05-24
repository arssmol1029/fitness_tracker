from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import forms
from django.contrib.auth.decorators import login_required
from .models import Workout, Exercise, WorkoutExercise, ExerciseSet
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.urls import reverse
from django.db.models import Q, Prefetch, Count
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from .services import WorkoutCalendar
from django.core.exceptions import ValidationError
from datetime import datetime
from .serializers import WorkoutSerializer, ExerciseSerializer


@login_required
def mainPage(request):
    date = timezone.now().date()

    workouts = Workout.objects.filter(user=request.user, date=date, is_template=False).annotate(
        exercise_count=Count('exercises')
    )


    try:
        year = int(request.GET.get('year', timezone.now().year))
        month = int(request.GET.get('month', timezone.now().month))
        
        if not (1 <= month <= 12):
            raise ValidationError("Некорректный месяц")
        if year < 2000 or year > 2100:
            raise ValidationError("Некорректный год")
            
    except:
        year, month = timezone.now().year, timezone.now().month

    calendar_data = WorkoutCalendar.get_month_data(request.user, year=year, month=month)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(calendar_data)


    return render(request, 'tracker/main-page.html', {
        'workouts': workouts,
        'calendar': calendar_data
    })


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
@api_view(['GET'])
def profilePage(request):
    user = request.user
    return render(request, 'base/profile.html', {'user': user})



@login_required
@api_view(['GET'])
def workoutListView(request):
    template_view = request.GET.get('templates', '').lower() == 'true'

    workouts = Workout.objects.filter(
        Q(user=request.user) | Q(is_custom=False)
    ).annotate(exercise_count=Count('exercises'))

    return render(request, 'tracker/workouts/list.html', {
        'workouts': workouts,
        'template_view': template_view
    })



@login_required
def workoutDayListView(request):
    try:
        date_str = request.GET.get('date', timezone.now().year)
        date = datetime.strptime(date_str, '%Y-%m-%d').date()    
    except:
        date = timezone.now().date()

    workouts = Workout.objects.filter(user=request.user, date=date, is_template=False).annotate(
        exercise_count=Count('exercises')
    )
    return render(request, 'tracker/workouts/day-list.html', {
        'date': date,
        'date_str': date.strftime('%Y-%m-%d'),
        'workouts': workouts
    })



@login_required
def workoutCreateView(request): 
    if request.method == 'POST':
        is_template_data = request.POST.get('is_template', 'false') == 'true'
        return workoutSave(request, is_template=is_template_data, is_new=True)
    else:
        try:
            date_str = request.GET.get('date', timezone.now().year)
            date = datetime.strptime(date_str, '%Y-%m-%d').date()    
        except:
            date = timezone.now().date()
        form = forms.WorkoutForm(initial={'date': date})

    return render(request, 'tracker/workouts/workout.html', {'form': form})



@login_required
def workoutEditView(request, pk):
    try:
        workout = Workout.objects.prefetch_related(
            Prefetch(
                'workoutexercise_set',
                queryset=WorkoutExercise.objects.order_by('order').select_related('exercise').prefetch_related(
                    Prefetch(
                        'exercise_sets',
                        queryset=ExerciseSet.objects.order_by('order'),
                        to_attr='ordered_sets'
                    )
                ),
                to_attr='workout_exercises'
            )
        ).get(id=pk)
    except Workout.DoesNotExist:
        raise Http404("Тренировка не найдена")
    if (workout.user and workout.user != request.user):
        raise Http404("Тренировка создана другим пользователем")
    if request.method == 'GET':
        form = forms.WorkoutForm(instance=workout)
        return render(request, 'tracker/workouts/workout.html',
                {'form': form, 'workout': workout})
    else:
        is_template_data = request.POST.get('is_template', 'false') == 'true'
        if is_template_data == workout.is_template:
            WorkoutExercise.objects.filter(workout_id=workout.id).delete()
            return workoutSave(request, workout=workout, is_template=is_template_data, is_new=False)
        else:
            return workoutSave(request, is_template=is_template_data, is_new=True)



@login_required
@api_view(['GET'])
def workoutNotChangeView(request, pk):
    try:
        workout = Workout.objects.prefetch_related(
            Prefetch(
                'workoutexercise_set',
                queryset=WorkoutExercise.objects.order_by('order').select_related('exercise').prefetch_related(
                    Prefetch(
                        'exercise_sets',
                        queryset=ExerciseSet.objects.order_by('order'),
                        to_attr='ordered_sets'
                    )
                ),
                to_attr='workout_exercises'
            )
        ).get(id=pk)
    except Workout.DoesNotExist:
        raise Http404("Тренировка не найдена")
    if (workout.user and workout.user != request.user):
        raise Http404("Тренировка создана другим пользователем")
    form = forms.WorkoutForm(instance=workout, is_only_view=True)
    return render(request, 'tracker/workouts/workout_only_view.html',
            {'form': form, 'workout': workout})



@login_required
@api_view(['POST'])
def workoutSave(request, workout=None, is_template=False, is_new=True):
    form = forms.WorkoutForm(request.POST, instance=workout)
    if form.is_valid():
        workout = form.save(commit=False)
        if is_new and Workout.objects.filter(
            (Q(user=request.user) | Q(is_custom=False)) & Q(name=workout.name) & Q(is_template=is_template)
        ).exists():
            return JsonResponse({
                'status': 'error',
                'message': 'Тренировка с таким названием уже существует!',
                'redirect_url': 'error'
            })
        workout.user = request.user
        workout.is_template = is_template
        workout.save()

        exercises_data = json.loads(request.POST.get('exercises', '[]'))
        
        try:
            for i, ex in enumerate(exercises_data):
                workout_exercise = WorkoutExercise.objects.create(
                    workout_id=workout.id,
                    exercise_id=ex['exercise_id'],
                    order=i,
                )
                sets=ex['sets']
                for j, set in enumerate(sets):
                    ExerciseSet.objects.create(
                        workout_exercise_id=workout_exercise.id,
                        order=j,
                        reps=set['reps'],
                        weight=set.get('weight'),
                    )
        except:
            return JsonResponse({
                'status': 'error',
                'message': 'Ошибка сохранения!',
                'redirect_url': 'error'
            })


        return JsonResponse({'status': 'ok'})
    
    return JsonResponse({
        'status': 'error',
        'message': 'Ошибка сохранения!',
        'redirect_url': 'error'
    })



@api_view(['GET'])
def templateSearch(request):
    term = request.GET.get('term', '')
    templates = Workout.objects.filter(
        Q(is_template=True) & (Q(is_custom=False) | Q(user=request.user)) & Q(name__icontains=term.capitalize())
    )
    results = [{'id': template.id, 'text': template.name} 
               for template in templates]
    return Response({'results': results})



@api_view(['GET'])
def templateLoad(request, pk):
    try:
        workout = Workout.objects.prefetch_related(
            Prefetch(
                'workoutexercise_set',
                queryset=WorkoutExercise.objects.order_by('order').select_related('exercise').prefetch_related(
                    Prefetch(
                        'exercise_sets',
                        queryset=ExerciseSet.objects.order_by('order'),
                        to_attr='ordered_sets'
                    )
                ),
                to_attr='workout_exercises'
            )
        ).get(id=pk)
    except Workout.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Объект не существует!'})
    if (workout.user and workout.user != request.user):
        return JsonResponse({'status': 'error', 'message': 'Шаблон создан другим пользователем!'})
    if (workout.is_template == False):
        return JsonResponse({'status': 'error', 'message': 'Объект не ялвяется шаблоном!'})
    
    serializer = WorkoutSerializer(workout)
    return JsonResponse({'status': 'ok', 'data':serializer.data})



@login_required
@api_view(['POST', 'DELETE'])
def workoutDelete(request, pk):
    try:
        workout = Workout.objects.get(id=pk)
        workout.delete()
        return JsonResponse({'status': 'ok'})
    except Workout.DoesNotExist:
        return JsonResponse({'status': 'error',  'message': 'Объект не найден!'})



@login_required
@api_view(['POST'])
def exerciseCreate(request):
    name = request.POST.get('name')
    is_own_weight = request.POST.get('is_own_weight') == 'true'
    
    if Exercise.objects.filter(
            Q(name=name) & (Q(user=request.user) | Q(is_custom=False)) & Q(is_own_weight=is_own_weight)).exists():
        return JsonResponse({
            'status': 'error',
            'message': 'Упражнение с данным названием уже существует!'
        })

    print('meow')
    print(name, is_own_weight)
    print('meow')

    exercise = Exercise.objects.create(
        user=request.user,
        name=name.capitalize(),
        is_own_weight=is_own_weight,
        is_custom=True
    )
    
    serializer = ExerciseSerializer(exercise)

    print(serializer.data)

    return JsonResponse({
        'status': 'ok',
        'data': serializer.data
    })



@login_required
@api_view(['GET'])
def exerciseListView(request):
    exercises = Exercise.objects.filter(Q(user=request.user) | Q(is_custom=False))

    return render(request, 'tracker/exercises/list.html', {
        'exercises': exercises
    })



@login_required
@api_view(['POST', 'DELETE'])
def exerciseDelete(request, pk):
    try:
        exercise = Exercise.objects.get(id=pk)
        exercise.delete()
        return JsonResponse({'status': 'ok'})
    except Workout.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Объект не найден!'})



@login_required
@api_view(['GET'])
def exerciseSearch(request):
    term = request.GET.get('term', '')
    exercises = Exercise.objects.filter((Q(is_custom=False) | Q(user=request.user)) & Q(name__icontains=term.capitalize()))
    results = [{'id': exercise.id, 'text': exercise.name, 'is_own_weight': exercise.is_own_weight} 
               for exercise in exercises]
    return Response({'results': results})



def customErrorView(request, exception):
    error_message = str(exception) if exception else "Извините, запрошенная страница не существует."
    return render(request, '404.html', {'error_message': error_message}, status=404)