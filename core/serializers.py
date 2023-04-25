from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'nickname', 'avatar', 'header', 'description', 'locale')


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

