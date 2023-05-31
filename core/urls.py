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
    path('users/<str:user_id>/followers', views.UserFollowersView.as_view(), name='user_followers'),
    path('users/<str:user_id>/following', views.UserFollowingView.as_view(), name='user_following'),
    path('users/following', views.FollowingView.as_view(), name='following'),
    path('users/<str:user_id>/friends', views.FriendsView.as_view(), name='friends'),
    path('users/<str:user_id>/friends/requests', views.FriendRequestView.as_view(), name='friend_requests'),
    path('users/<str:user_id>/friends/requests/accept', views.FriendRequestAcceptView.as_view(), name='friend_request_accept'),
    path('users/<str:user_id>/friends/requests/reject', views.FriendRequestRejectView.as_view(), name='friend_request_reject'),
    path('users/<str:user_id>/friends/requests/cancel', views.FriendRequestCancelView.as_view(), name='friend_request_cancel'),
    path('profile/<str:username>', views.UserProfileView.as_view(), name='user_profile'),
    path('message-threads', views.MessageThreadView.as_view(), name='message_threads'),
    path('message-threads/<uuid:message_thread_id>', views.MessageThreadDetailView.as_view(), name='message_thread_detail'),     
    path('message-threads/<uuid:message_thread_id>/messages', views.MessageThreadMessageView.as_view(), name='messages'),
    path('message-threads/<uuid:message_thread_id>/messages/<uuid:message_id>', views.MessageThreadMessageDetailView.as_view(), name='message_detail'),
    path('notifications', views.NotificationView.as_view(), name='notifications'),
    path('notifications/<uuid:notification_id>', views.NotificationDetailView.as_view(), name='notification_detail'),
]
