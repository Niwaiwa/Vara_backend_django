from django.views.generic import TemplateView
from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


app_name = 'core'

urlpatterns = [
    path('users/signup', views.SignupView.as_view(), name='signup'),
    path('users/login', views.LoginView.as_view(), name='login'),
    path('users/logout', views.LogoutView.as_view(), name='logout'),
    path('token', TokenRefreshView.as_view(), name='token_refresh'),
]
