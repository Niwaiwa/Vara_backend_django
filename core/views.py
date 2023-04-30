from json import JSONDecodeError
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Following, Followers, Friends, FriendRequest
from .serializers import UserSignupSerializer, UserLoginSerializer, UserSerializer, UserProfileSerializer, \
    FollowingListSerializer, FollowersListSerializer, FriendsListSerializer, FriendRequestListSerializer
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

class UserFollowingView(views.APIView):

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id, is_active=True, is_staff=False, is_superuser=False)
        followings = Following.objects.filter(user=user)
        serializer = FollowingListSerializer(followings, many=True)
        return Response(serializer.data)

class FollowingView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = JSONParser().parse(request)
            user_id = data.get('user_id')
            if not user_id:
                return Response({"result": 'error', 'message': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

            user = get_object_or_404(User, pk=user_id, is_active=True, is_staff=False, is_superuser=False)
            if user == request.user:
                return Response({"result": 'error', 'message': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

            following = Following.objects.filter(user=request.user, following_user=user)
            if following:
                return Response({"result": 'error', 'message': 'You are already following this user'}, status=status.HTTP_400_BAD_REQUEST)

            following = Following.objects.create(user=request.user, following_user=user)
            followe = Followers.objects.create(user=user, follower_user=request.user)
            return Response({"result": 'success', 'message': f'You are now following {user.username}!'}, status=status.HTTP_200_OK)
        except JSONDecodeError:
            return JsonResponse({"result": 'error', 'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            data = JSONParser().parse(request)
            user_id = data.get('user_id')
            if not user_id:
                return Response({"result": 'error', 'message': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            user = get_object_or_404(User, pk=user_id, is_active=True, is_staff=False, is_superuser=False)

            following = Following.objects.filter(user=request.user, following_user=user)
            if not following:
                return Response({"result": 'error', 'message': 'You are not following this user'}, status=status.HTTP_400_BAD_REQUEST)
            following.delete()
            follower = Followers.objects.filter(user=user, follower_user=request.user)
            if follower:
                follower.delete()
            return Response({"result": 'success', 'message': f'You are no longer following {user.username}!'}, status=status.HTTP_200_OK)
        except JSONDecodeError:
            return JsonResponse({"result": 'error', 'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

class UserFollowersView(views.APIView):
    
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id, is_active=True, is_staff=False, is_superuser=False)
        followers = Followers.objects.filter(user=user)
        serializer = FollowersListSerializer(followers, many=True)
        return Response(serializer.data)

class FriendsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        friends = Friends.objects.filter(user=request.user)
        serializer = FriendsListSerializer(friends, many=True)
        return Response(serializer.data)
    
    def post(self, request, user_id):
        try:
            data = JSONParser().parse(request)
            request_user_id = data.get('user_id')
            if not request_user_id:
                return Response({"result": 'error', 'message': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

            user = get_object_or_404(User, pk=request_user_id, is_active=True, is_staff=False, is_superuser=False)
            if user == request.user:
                return Response({"result": 'error', 'message': 'You cannot add yourself as a friend'}, status=status.HTTP_400_BAD_REQUEST)
            
            friend = Friends.objects.filter(user=request.user, friend=user)
            if friend:
                return Response({"result": 'error', 'message': 'You are already a friend of this user'}, status=status.HTTP_400_BAD_REQUEST)

            friend_request = FriendRequest.objects.filter(from_user=request.user, to_user=user)
            if friend_request:
                return Response({"result": 'error', 'message': 'You already sent a friend request to this user'}, status=status.HTTP_400_BAD_REQUEST)
            
            friend_request = FriendRequest.objects.create(from_user=request.user, to_user=user)
            return Response({"result": 'success', 'message': f'You sent a friend request to {user.username}!'}, status=status.HTTP_200_OK)
        except JSONDecodeError:
            return JsonResponse({"result": 'error', 'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, user_id):
        try:
            data = JSONParser().parse(request)
            request_user_id = data.get('user_id')
            if not request_user_id:
                return Response({"result": 'error', 'message': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            user = get_object_or_404(User, pk=request_user_id, is_active=True, is_staff=False, is_superuser=False)

            friend = Friends.objects.filter(user=request.user, friend=user)
            if not friend:
                return Response({"result": 'error', 'message': 'You are not a friend of this user'}, status=status.HTTP_400_BAD_REQUEST)
            friend.delete()
            friend = Friends.objects.filter(user=user, friend=request.user)
            if friend:
                friend.delete()
            return Response({"result": 'success', 'message': f'You are no longer a friend of {user.username}!'}, status=status.HTTP_200_OK)
        except JSONDecodeError:
            return JsonResponse({"result": 'error', 'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        
class FriendRequestView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        friend_requests = FriendRequest.objects.filter(to_user=request.user)
        serializer = FriendRequestListSerializer(friend_requests, many=True)
        return Response(serializer.data)

class FriendRequestAcceptView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            data = JSONParser().parse(request)
            request_user_id = data.get('user_id')
            if not request_user_id:
                return Response({"result": 'error', 'message': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            user = get_object_or_404(User, pk=request_user_id, is_active=True, is_staff=False, is_superuser=False)

            friend_request = FriendRequest.objects.filter(from_user=user, to_user=request.user)
            if not friend_request:
                return Response({"result": 'error', 'message': 'You have no friend request from this user'}, status=status.HTTP_400_BAD_REQUEST)
            friend_request.delete()
            friend = Friends.objects.create(user=request.user, friend=user)
            friend = Friends.objects.create(user=user, friend=request.user)
            return Response({"result": 'success', 'message': f'You are now friends with {user.username}!'}, status=status.HTTP_200_OK)
        except JSONDecodeError:
            return JsonResponse({"result": 'error', 'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

class FriendRequestRejectView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            data = JSONParser().parse(request)
            request_user_id = data.get('user_id')
            if not request_user_id:
                return Response({"result": 'error', 'message': 'user_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            user = get_object_or_404(User, pk=request_user_id, is_active=True, is_staff=False, is_superuser=False)

            friend_request = FriendRequest.objects.filter(from_user=user, to_user=request.user)
            if not friend_request:
                return Response({"result": 'error', 'message': 'You have no friend request from this user'}, status=status.HTTP_400_BAD_REQUEST)
            friend_request.delete()
            return Response({"result": 'success', 'message': f'You rejected the friend request from {user.username}!'}, status=status.HTTP_200_OK)
        except JSONDecodeError:
            return JsonResponse({"result": 'error', 'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
