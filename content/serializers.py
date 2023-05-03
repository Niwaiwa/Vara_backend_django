from rest_framework import serializers
from .models import Video, Tag


class VideoSerializer(serializers.ModelSerializer):
    VIDEO_RATING_CHOICES = [
        ('G', 'General'),
        ('E', 'Ecchi'),
    ]
    rating = serializers.ChoiceField(choices=VIDEO_RATING_CHOICES, source='get_rating_display')

    class Meta:
        model = Video
        fields = '__all__'


class VideoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('title', 'description', 'video_file', 'video_url', 'rating', 'tags')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'views_count', 'likes_count')


class VideoPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ('title', 'description', 'rating', 'tags')
        read_only_fields = ('id', 'user', 'video_file', 'video_url', 'created_at', 'updated_at', 'views_count', 'likes_count')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name',)
