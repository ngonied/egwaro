from rest_framework import serializers
from .models import *
#from rest_framework.fields import CurrentUserDefault

class SyllabusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Syllabus
        fields = '__all__'


class LevelSerializer(serializers.ModelSerializer):
    syllabus_name = serializers.SerializerMethodField('get_syllabus')

    class Meta:
        model = Level
        fields = ['id', 'name', 'syllabus',
                  'description', 'syllabus_name']

    def get_syllabus(self, syllabus):
        syllabus_name = syllabus.syllabus.name
        return syllabus_name


class SubjectSerializer(serializers.ModelSerializer):
    syllabus_name = serializers.SerializerMethodField('get_syllabus_name')
    level_name = serializers.SerializerMethodField('get_level_name')

    class Meta:
        model = Subject
        fields = ['id', 'name', 'description',
                  'image', 'syllabus_name', 'code', 'level_name']

    def get_syllabus_name(self, subject):
        syllabus_name = subject.level.syllabus.name
        return syllabus_name

    def get_level_name(self, subject):
        level_name = subject.level.name
        return level_name


class CourseSerializer(serializers.ModelSerializer):
    written_by = serializers.SerializerMethodField('get_author')
    subject_name = serializers.SerializerMethodField('get_subject_name')
    enrolled = serializers.SerializerMethodField('check_if_enrolled')


    def get_author(self, course):
        written_by = course.created_by.email
        return written_by

    def get_subject_name(self, course):
        subject_name = course.subject.name
        return subject_name
    
    def check_if_enrolled(self, course):
        enrolled = False
        if self.context['request'].user.is_authenticated:
            
            course_enrolled = Enrol.objects.filter(course = course).filter(student = self.context['request'].user)
            #.filter(student = CurrentUserDefault())
            
            if course_enrolled:
                enrolled = True
            
               

        return enrolled

    class Meta:
        model = Course
        fields = ['id', 'name', 'image', 'description', 'subject',
                  'created_by', 'subject_name', 'written_by', 'enrolled']

    

class CourseKeyPointSerializer(serializers.ModelSerializer):
    # topics = serializers.SerializerMethodField('get_topics')

    class Meta:
        model = CourseKeyPoint
        fileds = [
            'course',
            'description',
            'covered',
            'average_course_score',
            #'topics' #topics(material) within the course
        ]
        
    # def get_topics(self, coursekeypoint):
    #     course = coursekeypoint.course
    #     topics = Topic.objects.filter(course = course)
    #     return topics
            
            

class TopicSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField('get_course_name')

    class Meta:
        model = Topic
        fields = ['id', 'name', 'description', 'course',
                  'course_name', 'image', 'file1', 'content', 'video', 'average_score', 'studying']

    def get_course_name(self, topic):
        course_name = topic.course.name
        return course_name

class TopicListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField('get_status')

    class Meta:
        model = Topic
        fields = ['id', 'name', 'description', 'course', 'image', 'average_score', 'studying', 'status']

    def get_status(self, topic):
        status = topic.get_studying_display()
        return status

class IllustrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Illustration
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = '__all__'


class EnrolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrol
        fields = '__all__'
