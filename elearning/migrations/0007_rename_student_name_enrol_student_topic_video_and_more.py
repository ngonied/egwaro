# Generated by Django 4.0.1 on 2022-01-21 19:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0006_alter_subject_code'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enrol',
            old_name='student_name',
            new_name='student',
        ),
        migrations.AddField(
            model_name='topic',
            name='video',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='enrol',
            name='progress',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(0)]),
        ),
    ]
