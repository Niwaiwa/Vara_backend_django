from json import JSONDecodeError
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import views, status
from rest_framework.parsers import JSONParser


from .serializers import UserSignupSerializer, UserLoginSerializer, UserSerializer


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
