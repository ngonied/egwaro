from rest_framework import status, permissions #problem with status here
from rest_framework.views import APIView
from rest_framework.response import Response # This class has a problem
from rest_framework_simplejwt import views as jwt_views # We have TokenObtainView and TokenRefreshView in here
from .serializers import  UserSerializer #My CustomUser serializer
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser, FormParser




class CreateCustomUser(APIView):
    #parser_classes = (MultiPartParser, FormParser)
    #register a user and obtain a token in one view
    permission_classes = (permissions.AllowAny,)
    authenticaton_classes = ()

    def post(self, request, format = 'json'):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = request.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        
        serializer = UserSerializer(request.user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        # serializer =UserSerializer(request.user, data =request.data, partial =True)
        serializer =UserSerializer(request.user, data =request.data, partial =True)
        print("this is the request: ")
        print(request.data)
        print("Here is the user: ")
        print(request.user)


        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_400_BAD_REQUEST)



class LogoutBlackListRefreshTokenView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        print(request.data)
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)