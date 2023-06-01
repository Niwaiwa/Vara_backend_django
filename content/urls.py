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
    path('images/<uuid:images_id>/comments', views.ImageSlideCommentListCreateAPIView.as_view(), name='imageslide_comment_list'),
    path('images/<uuid:images_id>/comments/<uuid:comment_id>', views.ImageSlideCommentDetailAPIView.as_view(), name='imageslide_comment_detail'),
    path('playlists', views.PlaylistAPIView.as_view(), name='playlist_list'),
    path('playlists/<uuid:playlist_id>', views.PlaylistDetailAPIView.as_view(), name='playlist_detail'),
    path('playlists/<uuid:playlist_id>/<uuid:video_id>', views.PlaylistVideoAPIView.as_view(), name='playlist_video'),
    path('posts', views.PostAPIView.as_view(), name='post_list'),
    path('posts/<uuid:post_id>', views.PostDetailAPIView.as_view(), name='post_detail'),
    path('posts/<uuid:post_id>/comments', views.PostCommentListCreateAPIView.as_view(), name='post_comment_list'),
    path('posts/<uuid:post_id>/comments/<uuid:comment_id>', views.PostCommentDetailAPIView.as_view(), name='post_comment_detail'),
    path('profile/<uuid:user_id>/comments', views.ProfileCommentListCreateAPIView.as_view(), name='profile_comment_list'),
    path('profile/<uuid:user_id>/comments/<uuid:comment_id>', views.ProfileCommentDetailAPIView.as_view(), name='profile_comment_detail'),
    path('forum', views.ForumAPIView.as_view(), name='forum_list'),
    path('forum/<uuid:forum_id>', views.ForumDetailAPIView.as_view(), name='forum_detail'),
    path('forum/<uuid:forum_id>/threads', views.ForumThreadAPIView.as_view(), name='forum_thread_list'),
    path('forum/<uuid:forum_id>/threads/<uuid:thread_id>', views.ForumThreadDetailAPIView.as_view(), name='forum_thread_detail'),
    path('forum/<uuid:forum_id>/threads/<uuid:thread_id>/posts', views.ForumPostAPIView.as_view(), name='forum_thread_post_list'),
    path('forum/<uuid:forum_id>/threads/<uuid:thread_id>/posts/<uuid:post_id>', views.ForumPostDetailAPIView.as_view(), name='forum_thread_post_detail'),
]