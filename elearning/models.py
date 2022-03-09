from django.db import models
from django.db.models.fields import AutoField
from django.db.models.fields.files import FileField, ImageField
from users.models import CustomUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# syllabus is the head of all things courses No.1
class Syllabus(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    syllabus_file = models.FileField(
        upload_to="files/syllabuses", blank=True, null=True)
    logo = models.ImageField(
        upload_to="files/syllabuses", blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def syllabus_name(self):
        return self.name


class Level(models.Model):
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


    @property
    def level_name(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=255, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="files/icons", blank=True, null=True)
    code = models.CharField(max_length=15, null=False,
                            unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=255, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="files/icons", blank=True, null=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class CourseKeyPoint(models.Model):
    course = models.ForeignKey(Course, on_delete = models.CASCADE)
    description = models.TextField(null = True, blank = True)
    covered = models.BooleanField(default = False)
    average_key_point_score = models.IntegerField(default=0, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])


class Topic(models.Model):
    name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=255, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to="files/icons", blank=True, null=True)
    file1 = models.FileField(upload_to="files/material", blank=True, null=True)
    content = models.TextField(null=True)
    video  = models.CharField(max_length = 200, null = True)

    def __str__(self):
        return self.name


class Illustration(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    notes = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to="files/diagrams", blank=True)


class Assignment(models.Model):
    name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=255, blank=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    release_date = models.DateField(auto_now=True)
    submission_date = models.DateField(blank=True, null=True)
    file1 = models.FileField(
        upload_to="files/assignments", blank=True, null=True)
    created_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Response(models.Model):
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, null=True)
    file1 = models.FileField(upload_to="files/assignments", null=True)
    submitted_by = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True)
    score = models.IntegerField(default=0, validators=[
        MaxValueValidator(100),
        MinValueValidator(1)
    ])
    comments = models.TextField(blank=True)

    def __str__(self):
        return self.assignment


class Exercise(models.Model):
    pass


class question(models.Model):
    pass


class Enrol(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    in_progress = models.BooleanField(default=True)
    complete = models.BooleanField(default=False)
    date = models.DateField(auto_now=True)


    def __str__(self):
        details = str(self.student.email  + " has enrolled for " + self.course.name)
        return details
     
