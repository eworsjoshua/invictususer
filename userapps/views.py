from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .serializers import ProfileSerializer, RegistrationSerializer
from .models import profile as Profile


# REGISTRATION VIEW
class RegistrationView(APIView):
    def post(self, request):
        try:
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Login VIEW
class LoginView(APIView):
    def post(self, request):
        try:
            username= request.data.get('username')
            password= request.data.get ('password')
            user = authenticate (username=username, password=password)
            if user is not None:
                login(request, user)
                return Response ({"Message": "Login Successful"}, status=status.HTTP_200_OK)
            return Response ({"Message": "Invalid username/Password"}, status=status.HTTP_400_BAD_REQUEST)
                 
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    #  Dashboard VIEW
class UserDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
           profile_obj = Profile.objects.get(user=request.user)
           serializer = ProfileSerializer(profile_obj)
           data = serializer.data
           return Response(data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)            

 #  Logout VIEW
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            logout(request)
            return Response({"Message": "Logout Successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)        
          