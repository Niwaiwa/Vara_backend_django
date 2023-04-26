from json import JSONDecodeError
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import UserSignupSerializer, UserLoginSerializer, UserSerializer, UserProfileSerializer
from .utils import get_tokens_for_user


class SignupView(views.APIView):
    
    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = UserSignupSerializer(data=data)
            if serializer.is_valid():
                user = serializer.save()
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": 'error', 'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(views.APIView):

    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = UserLoginSerializer(data=data)
            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                user = authenticate(request, username=username, password=password)
                if user:
                    if not user.is_active:
                        return Response({"result": 'error', 'message': 'User account is disabled.'}, status=status.HTTP_401_UNAUTHORIZED)
                    login(request, user)
                    auth_token = RefreshToken.for_user(request.user)
                    # return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
                    return Response({'token': str(auth_token)}, status=status.HTTP_200_OK)
                else:
                    return Response({"result": 'error', 'message': 'Unable to log in with provided credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": 'error', 'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"result": 'success', 'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)

class UserProfileView(views.APIView):

    def get(self, request, username):
        user = get_object_or_404(User, username=username, is_active=True, is_staff=False, is_superuser=False)
        return Response(UserProfileSerializer(user).data, status=status.HTTP_200_OK)

class UserView(views.APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
    
    def put(self, request):
        data = request.data
        serializer = UserSerializer(request.user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
