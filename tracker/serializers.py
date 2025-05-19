from rest_framework import serializers
from .models import Workout, Exercise, WorkoutExercise, ExerciseSet

class ExerciseSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseSet
        fields = ['id', 'order', 'reps', 'weight']

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    ordered_sets = ExerciseSetSerializer(many=True, source='exercise_sets')
    exercise_name = serializers.CharField(source='exercise.name')
    exercise_id = serializers.IntegerField(source='exercise.id')
    is_own_weight = serializers.BooleanField(source='exercise.is_own_weight')
    
    class Meta:
        model = WorkoutExercise
        fields = ['id', 'order', 'exercise_id', 'exercise_name', 'is_own_weight', 'ordered_sets']

class WorkoutSerializer(serializers.ModelSerializer):
    workout_exercises = WorkoutExerciseSerializer(many=True, source='workoutexercise_set')
    
    class Meta:
        model = Workout
        fields = ['id', 'name', 'date', 'is_template', 'is_custom', 'workout_exercises']

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'is_custom', 'is_own_weight']