from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import DO_NOTHING
from django.db.models.fields.related import ForeignKey, OneToOneField
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


#  Subject: Has a one to many relationship with Course
# 	    Ha	s a one to many relation with Tutor
# 	    Has a many to relationship with Student
# name
# courses one to many-to-may
# students

class Subject(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Course: has a many to many relationship with Student
# 	    has a many to many relationship with with Tutor
# 1. Name = Charfield
# 2. Subject = foreignkey(Subject) many-to-one
# 3. students = foreignkey(Student)many-to-many
# 4.  Progress

class Course(models.Model):
    name = models.CharField(max_length=50)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Topic: has many to one relationship with Assignment
# 	 has a one to one relationship Course

class Topic(models.Model):
    name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_progress = models.IntegerField(default=0)

    def __str__(self):
        return self.name


"""The plan on Topic and TopicInstances is this, a topic will have multiple instances of that topic.
instances will have order using the order field which is used to sort the TopicInstances. Multiple
sorted instances will be combined to form a single page content to be viewed as a whole; material for that
Topic. Custom CMS that is. """


# class TopicInstance(models.Model):
#     topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
#     content = models.TextField()
#     order = models.IntegerField()
#     diagram = models.ImageField(
#         upload_to='topic_diagrams', blank=True, required=False)


# The link to profile has been ceased
# Establish it here linking subject/user instead
# This part will be left out for now
class Statistic(models.Model):
    pass


# Profile: Has a one to one relation with a Student
#  name = foreign_key through username(Student)
# picture = ImageField
# Bio
# foreign_key to courses
# foreign_key to stats

# There is a good chance that this is what you want.
# Personally that is the method I use for
#  the most part. We will be creating a new Django Model to
#  store the extra information that relates to the User Model.

# Bear in mind that using this strategy results in
# additional queries or joins to retrieve the related data. Basically all
# the time you access an related data, Django will fire an additional query.
# But this can be avoided for the most cases. I will get back to that later on.
# Now this is where the magic happens: we will now define signals so our Profile model
# will be automatically created/updated when we create/update User instances.
# Basically we are hooking the create_user_profile and save_user_profile methods to the User model, whenever a save event occurs. This kind of signal is called post_save.

# Great stuff. Now, tell me how can I use it.

# Piece of cake. Check this example in a Django Template:
# <h2>{{ user.get_full_name }}</h2>
# <ul>
#   <li>Username: {{ user.username }}</li>
#   <li>Location: {{ user.profile.location }}</li>
#   <li>Birth Date: {{ user.profile.birth_date }}</li>
# </ul>
# How about inside a view method?

# def update_profile(request, user_id):
#     user = User.objects.get(pk=user_id)
#     user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
#     user.save()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(
        max_length=30, default="Somewhere in Cape Town")
    birth_date = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to='profile_pics', blank=True)
    #subject = models.ManyToManyField(Subject, blank=True)
    is_tutor = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username


class Assignment(models.Model):

    name = models.CharField(max_length=50)
    date_issued = models.DateField(auto_now=True)
    date_due = models.DateField(auto_now=False)
    # topic = models.ManyToManyField(Profile)
    assign_out = models.FileField(upload_to='assign_out')
    subject = ForeignKey(Subject, on_delete=DO_NOTHING, default=1)

    def __str__(self):
        return self.name


class Answer(models.Model):
    answer = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    assign_in = models.ForeignKey(Profile, on_delete=models.CASCADE)
    file = models.FileField(upload_to='inbound_assgns')
    submission = models.DateField(auto_now=True)

    def __str__(self):
        display_name = (self.answer.name +
                        " answer from: " + self.assign_in.user.username)
        return display_name


class AssignmentFeedback(models.Model):
    feedback = models.OneToOneField(Answer, on_delete=models.CASCADE)
    comment = models.TextField()
    assessed_doc = models.FileField(upload_to='assessed_docs')


class CourseStarted(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)
