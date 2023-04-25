from django.views.generic import TemplateView
from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'core'

urlpatterns = [
    path('users/signup', views.SignupView.as_view(), name='signup'),
]
