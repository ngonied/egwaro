from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('user', 'bio', 'location', 'birth_date', 'photo')


class AssignmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Assignment
        fields = "__all__"


# class TopicInstanceSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = TopicInstance
#         fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = "__all__"


# class TopicSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Topic
#         fields = "__all__"


class SubjectDetail(serializers.Serializer):

    subject_list = SubjectSerializer(many=True)
    course_list = CourseSerializer(many=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],

        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class CourseStartedSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseStarted
        fields = "__all__"
