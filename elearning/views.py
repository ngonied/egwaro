from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status, permissions
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response as MyResponse
from django.shortcuts import get_object_or_404
#from rest_framework.decorators import api_view
from datetime import date

from .models import *
from .serializers import *


# class EnrolForCourseView(APIView):
#     # def get(self, request):
#     #     data = Enrol.objects.filter(student_name=request.user)
#     #     serializer = EnrolSerializer(data=data, many=True)
#     #     if serializer.is_valid:
#     #         return Response(serializer.data)
#     #     else:
#     #         return Response(serializer.errors)

#     def post(self, request):
#         data = {'course': request.data.get("course"), 
#         'student': request.user.id, "progress":0, 
#         "completed":False, "in_progress":True, 
#         "date":date.today()}

#         serializer = EnrolSerializer(
#             data= data, many=True)
#         #queryset = Enrol.objects.filter(student_name=request.user)
#         print(request.data )
#         print(request.user)
#         print("The data is" )
#         print(data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return MyResponse(serializer.data, status=status.HTTP_201_CREATED)
#         return MyResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# @api_view(('POST',))
# def EnrolForCourseView(request):
#     if request.method == 'POST':
#         serializer = EnrolSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(str(serializer.data))
#     else:
#         return Response(str(serializer.errors))

    





"""This view is only for listing levels under a particular syllabus
it does not create them"""


class AllLevelsListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = [permissions.IsAuthenticated]


class SyllabusListView(generics.ListCreateAPIView):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer
    permission_classes = [permissions.IsAuthenticated]

class AllCoursesListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class AllSubjectsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

# Levels offered for a particular syllabus


class SyllabusLevelsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queryset = Level.objects.filter(
            syllabus__name__exact=self.kwargs["syllabus"])
        return queryset
    serializer_class = LevelSerializer


class MyCoursesView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queryset = Course.objects.all()
        
        return queryset

    serializer_class = CourseSerializer
    


# class SyllabusLevelsView(generics.ListAPIView):
#     serialializer_class = LevelSerializer

#     def get_queryset(self):
#         syllabus_name = self.kwargs['syllabus']
#         queryset = Level.objects.filter(syllabus=syllabus_name)
#         return queryset

# Subjects available in a particular Level
class LevelSubjectsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queryset = Subject.objects.filter(
            level__id__exact=self.kwargs["id"])
        return queryset
    serializer_class = SubjectSerializer


class SubjectCoursesView(generics.ListAPIView):
    def get_queryset(self):
        queryset = Course.objects.filter(
            subject__code__exact=self.kwargs["code"])
        return queryset
    serializer_class = CourseSerializer


class CourseTopicsView(generics.ListAPIView):
    def get_queryset(self):
        queryset = Topic.objects.filter(
            course__exact=self.kwargs["pk"])
        return queryset
    serializer_class = TopicListSerializer


class CourseKeyPointsView(generics.ListAPIView):
    def get_queryset(self):
        queryset = CourseKeyPoint.objects.filter(
            course__id__exact=self.kwargs["course_id"])
        return queryset
    serializer_class = TopicListSerializer

class TopicDetailsView(generics.RetrieveAPIView):
    look_up_field = 'id'
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class CourseDetailView(APIView):
    def get(self, request, pk):
        print(request)
        queryset = get_object_or_404(Course, pk=pk)
        print(queryset)
        serializer = CourseSerializer(queryset, context={"request": request})
        return MyResponse(serializer.data, status=status.HTTP_200_OK )
    



# class EnrolForCourseView(APIView):
#     # serializer_class = EnrolSerializer

#     def post(self, request):
#         serializer = EnrolSerializer(data = request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"status": "success", "data": serializer.data})

#         else:
#             return Response ({"status": "error", "data": serializer.errors})
        
        # #content = {'status': 'bad request'}
        # print(self.request.data)
        # course = Course.objects.filter(id=request.data.get("course"))
        # data = {'course': course, 'student': request.user}
        # print(data)
        # serializer = EnrolSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     # return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        #     return Response(serializer.data)
        # else:
        #     return Response(serializer.errors)


# class PollList(APIView):
#     def get(self, request):
#         polls = Poll.objects.all()[:20]
#         data = PollSerializer(polls, many=True).data
#         return Response(data)


# class PollDetail(APIView):
#     def get(self, request, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         data = PollSerializer(poll).data
#         return Response(data)


# class PollList(generics.ListCreateAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer

# class PollDetail(generics.RetrieveDestroyAPIView):
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer
#     RetrieveDestroyAPIView
#     ListCreateAPIView
#     CreateAPIView


class EnrolForCourseView(ModelViewSet):
    queryset = Enrol.objects.none()
    serializer_class = EnrolSerializer
    permission_classes = [permissions.IsAuthenticated,]
    http_method_names = ['post', ]

    def create(self, request, *args, **kwargs):
        student = request.user
        course = request.data.get("course")
        data = {
            "student": student.id,
            "course": course
        }

        _serializer = self.serializer_class(data=data)  
        if _serializer.is_valid():
            _serializer.save()
            return MyResponse(data=_serializer.data, status=status.HTTP_201_CREATED)  
       
        return MyResponse(data=_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
