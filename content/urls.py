from django.views.generic import TemplateView
from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


app_name = 'content'

urlpatterns = [
    path('videos', views.VideoListCreateAPIView.as_view(), name='video_list'),
    path('videos/<str:pk>', views.VideoDetailAPIView.as_view(), name='video_detail'),
    path('tags', views.TagAPIView.as_view(), name='tag_list'),
]