from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import SignUpForm, ExerciseForm, WorkoutForm
from django.contrib.auth.decorators import login_required
from .models import Workout

@login_required
def mainPage(request):
    global_workouts = Workout.objects.filter(is_custom = False)
    custom_workouts = Workout.objects.filter(user = request.user)

    return render(
        request,
        'tracker/main_page.html',   
        {
            'global_workouts': global_workouts,
            'custom_workouts': custom_workouts,
        },
    )

def signup(request):
    if request.user.is_authenticated:
        return redirect('main_page')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main_page')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})

@login_required
def addCustomExercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(False)
            exercise.user = request.user
            exercise.is_custom = True
            exercise.save()
            return redirect('main_page')
    else:
        form = ExerciseForm()
    
    return render(request, 'tracker/exercises/new_custom_exercise.html', {'form': form})
        

def newWorkout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('main_page')
    else:
        form = WorkoutForm(user=request.user)

    return render(request, 'tracker/workouts/new_workout.html', {'form': form})

def editWorkout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)

    return render(request, 'tracker/workouts/edit_workout.html', {'workout': workout})

