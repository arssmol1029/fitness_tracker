# Generated by Django 5.2 on 2025-05-16 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0009_rename_workoutexercises_workoutexercise'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workout',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='workout',
            name='is_template',
            field=models.BooleanField(db_index=True, default=False),
        ),
    ]
