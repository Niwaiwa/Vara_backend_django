from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Following, Followers

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'nickname', 'avatar', 'header', 'description')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'nickname', 'avatar', 'header', 'description', 'locale')
        read_only_fields = ('username',)

class UserSignupSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    def save(self):
        user = User(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
        )
        password1 = self.validated_data['password1']
        password2 = self.validated_data['password2']
        if password1 != password2:
            raise serializers.ValidationError("Passwords do not match")
        user.set_password(password1)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        extra_kwargs = {'password': {'write_only': True, 'required': True, 'style': {'input_type': 'password'}}}


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True, 'style': {'input_type': 'password'}}}

class FollowingListSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='following_user.username')
    avatar = serializers.ImageField(source='following_user.avatar')
    nickname = serializers.ReadOnlyField(source='following_user.nickname')

    class Meta:
        model = Following
        fields = ('user_name', 'nickname', 'avatar', 'created_at', 'updated_at')

class FollowersListSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='follower_user.username')
    avatar = serializers.ImageField(source='follower_user.avatar')
    nickname = serializers.ReadOnlyField(source='follower_user.nickname')

    class Meta:
        model = Followers
        fields = ('user_name', 'nickname', 'avatar', 'created_at', 'updated_at')
