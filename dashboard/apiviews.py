from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Course
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated


class CourseList(APIView):
    def get(self, request):
        courses = Course.objects.all()[:20]
        data = CourseSerializer(courses, many=True).data
        return Response(data)


class CourseDetail(APIView):

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        data = CourseSerializer(course).data
        return Response(data)


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})

        else:
            return Response({"error": "Wrong Credentials"})


class ProfilesList(generics.ListCreateAPIView):
    permission_classes = ()

    def get_queryset(self):
        query_set = Profile.objects.filter(is_tutor=False)
        return query_set
        # data = ProfileSerializer(profile_list, many=True).data
        # return Response(data)
    serializer_class = ProfileListSerializer


class ProfileView(APIView):
    permission_classes = ()

    def get(self, request, pk):
        profile = get_object_or_404(Profile, pk=pk)
        data = ProfileSerializer(profile).data

        return Response(data)


class UpdateProfile(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        # profile = get_object_or_404(Profile, user=request.user)

        profile = Profile.objects.get(user=request.user)
        # print(profile)
        # print(request.user)
        # data = {"user": request.user, "bio": request.data.get['bio'],
        #         "location": request.data.get['location'],
        #         "birth_date": request.data.get['birthdate'],
        #         "photo": request.data.get['photo']
        #         }
        if request.user == profile.user:
            info = request.data
            info['user'] = profile.id
            serializer = ProfileSerializer(data=info, instance=profile)
            if serializer.is_valid():
                new_info = serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)

        else:
            raise PermissionDenied(
                "You can not edit this Profile, it does not belong to you!")


class StartCourse(APIView):
    def post(self, request, *args, **kwargs):
        info = request.data
        info['student'] = request.user.id
        # coursename = request.data.get("course")
        # info = {'student': request.user.id, 'course': coursename}
        serializer = CourseStartedSerializer(data=info)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class SubjectDetail(APIView):
    def get(self, request, pk):
        subject_name = Subject.objects.get(pk=pk)
        course_list = Course.objects.filter(subject=subject_name)
        print(course_list)
        info = CourseSerializer(course_list).data
        # print(info)

        return Response(info)
