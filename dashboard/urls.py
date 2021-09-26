from django.contrib import admin
from django.urls import path
from .apiviews import *


urlpatterns = [
    path("courses/", CourseList.as_view(), name="courses"),
    path("course/<int:pk>/", CourseDetail.as_view(), name="course_detail"),
    path("users/", UserCreate.as_view(), name="create_user"),
    path("login/", LoginView.as_view(), name="login"),
    path("profiles/", ProfilesList.as_view(), name="profile"),
    path("profile_update/", UpdateProfile.as_view(),
         name="update_profile"),  # works don't fix it
    path("startcourse/", StartCourse.as_view(),
         name="start_course/"),  # needs attention
    path("subjectdetail/<int:pk>/", SubjectDetail.as_view()),  # not working

]
