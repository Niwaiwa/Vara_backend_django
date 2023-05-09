from django.views.generic import TemplateView
from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


app_name = 'content'

urlpatterns = [
    path('videos', views.VideoListCreateAPIView.as_view(), name='video_list'),
    path('videos/<uuid:pk>', views.VideoDetailAPIView.as_view(), name='video_detail'),
    path('videos/<uuid:pk>/like', views.VideoLikeAPIView.as_view(), name='video_like'),
    path('videos/<uuid:pk>/unlike', views.VideoUnlikeAPIView.as_view(), name='video_unlike'),
    path('videos/<uuid:video_id>/comments', views.VideoCommentListCreateAPIView.as_view(), name='video_comment_list'),
    path('videos/<uuid:video_id>/comments/<uuid:comment_id>', views.VideoCommentDetailAPIView.as_view(), name='video_comment_detail'),
    path('tags', views.TagAPIView.as_view(), name='tag_list'),
    path('images', views.ImageSlideListCreateAPIView.as_view(), name='imageslide_list'),
    path('images/<uuid:pk>', views.ImageSlideDetailAPIView.as_view(), name='imageslide_detail'),
    path('images/<uuid:pk>/like', views.ImageSlideLikeAPIView.as_view(), name='imageslide_like'),
    path('images/<uuid:pk>/unlike', views.ImageSlideUnLikeAPIView.as_view(), name='imageslide_unlike'),
    path('images/<uuid:images_id>/image', views.ImageListCreateAPIView.as_view(), name='image_list'),
    path('images/<uuid:images_id>/image/<uuid:pk>', views.ImageDetailAPIView.as_view(), name='image_detail'),
]