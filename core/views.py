from json import JSONDecodeError
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSignupSerializer, UserLoginSerializer, UserSerializer
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