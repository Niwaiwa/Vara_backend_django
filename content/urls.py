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
    path('images', views.ImageSlideListCreateAPIView.as_view(), name='imageslide_list'),
    path('images/<uuid:pk>', views.ImageSlideDetailAPIView.as_view(), name='imageslide_detail'),
    path('images/<uuid:images_id>/image', views.ImageListCreateAPIView.as_view(), name='image_list'),
    path('images/<uuid:images_id>/image/<uuid:pk>', views.ImageDetailAPIView.as_view(), name='image_detail'),
]