# Generated by Django 4.0.1 on 2022-01-27 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('elearning', '0007_rename_student_name_enrol_student_topic_video_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='level',
            options={'ordering': ['name']},
        ),
        migrations.AddField(
            model_name='enrol',
            name='date',
            field=models.DateField(auto_now=True),
        ),
    ]
