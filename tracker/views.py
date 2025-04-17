from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm, ExerciseForm, WorkoutForm
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    name = request.user.username
    return render(request, 'tracker/dashboard.html', {'name': name})

def signup(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
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
            return redirect('dashboard')
    else:
        form = ExerciseForm()
    
    return render(request, 'tracker/exercises/new_custom_exercise.html', {'form': form})
        

def newWorkout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = WorkoutForm(user=request.user)

    return render(request, 'tracker/workouts/new_workout.html', {'form': form})