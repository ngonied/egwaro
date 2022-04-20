from django.urls import path, re_path
from .views import *


urlpatterns = [
    # a list of levels in a curriculum, working
    re_path(r'^syllabuses/(?P<syllabus>\w+)/$', SyllabusLevelsView.as_view()),
    path("", AllCoursesListView.as_view()),  # a list of all courses, working
    path("syllabuses/", SyllabusListView.as_view(),  # a list of all syllabuses, working
         name="sylabuses_list"),
    re_path(r'^syllabuses/(?P<syllabus>\w+)/(?P<id>\w+)/$',  # a list of subjects in a level, working
            LevelSubjectsView.as_view(), name="sub_list"),
    re_path(r'^syllabuses/(?P<syllabus>\w+)/(?P<id>\w+)/(?P<code>\w+)/$',  # List of courses under a subject...
            SubjectCoursesView.as_view()),
    re_path(r'^syllabuses/(?P<syllabus>\w+)/(?P<id>\w+)/(?P<code>\w+)/(?P<pk>\w+)/$',  # List of topics under a subject...
            CourseTopicsView.as_view()),
    #     path("syllabuses/<str:syllabus>/<int:level>/<int:subject>/<int:course>/",  # list of topics
    #          CourseTopicsView.as_view(), name="topics_list"),
    #     path("syllabuses/<str:syllabus>/<int:level>/<int:course>/enrol/",  # enrol
    #          EnrolForCourseView.as_view(), name="enrol_view"),
    re_path(r'^courses/$', AllCoursesListView.as_view(),
         name="all_courses_list"),
    re_path(r'^courses/(?P<pk>[0-9]+)/$', CourseTopicsView.as_view(), name= "Course_details"), #We're here guys
    re_path(r'^my_courses/$', MyCoursesView.as_view(), name = "my_courses"),
    path("levels/", AllLevelsListView.as_view(), name='all_levels'),
    path("subjectslist/", AllSubjectsView.as_view()),
    re_path(r'subjectslist/(?P<code>\w+)/$', SubjectCoursesView.as_view(), name = "subject_courses_list"), #list of subj courses
    re_path(r'^enrol/$', EnrolForCourseView.as_view({'post':'create'}), name="enrol"),
    re_path(r'^courses/(?P<course_id>\w+)/topiclist/$', CourseTopicsView.as_view()),
    re_path(r'^courses/(?P<course_id>[0-9]+)/keypoints/$', CourseKeyPointsView.as_view()),
    re_path(r'^syllabuses/(?P<syllabus>\w+)/(?P<id>\w+)/(?P<code>\w+)/(?P<course_id>\w+)/(?P<pk>\w+)/$',  # List of topics under a subject...
            TopicDetailsView.as_view()),

]


""" paths are like so
     syllabuses --working
     syllabuses/Levels --working
     syllabus/levels/Subjects---working
     syllabus/Levels/Subjects/Courses
     syllabus/Levels/Subjects/Courses/Topics



"""
