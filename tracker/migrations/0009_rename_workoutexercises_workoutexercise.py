# Generated by Django 5.2 on 2025-05-08 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0008_rename_set_number_exerciseset_order_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='WorkoutExercises',
            new_name='WorkoutExercise',
        ),
    ]
