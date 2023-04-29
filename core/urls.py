from django.views.generic import TemplateView
from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


app_name = 'core'

urlpatterns = [
    path('token', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/signup', views.SignupView.as_view(), name='signup'),
    path('users/login', views.LoginView.as_view(), name='login'),
    path('users/logout', views.LogoutView.as_view(), name='logout'),
    path('users/user', views.UserView.as_view(), name='user_detail'),
    path('users/profile/<str:username>', views.UserProfileView.as_view(), name='user_profile'),
    path('users/<str:user_id>/following', views.UserFollowingView.as_view(), name='user_following'),
    path('users/following', views.FollowingView.as_view(), name='following'),
]
