from rest_framework import serializers
from .models import Video, Tag, ImageSlide, Image, VideoLike, ImageSlideLike, \
    VideoComment, ImageSlideComment, Playlist, Post, PostComment, ProfileComment


class UUIDField(serializers.Field):
    def to_representation(self, value):
        return str(value)


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


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

    def get_image_url(self, image):
        request = self.context.get('request')
        image_url = image.image_file.url
        return request.build_absolute_uri(image_url)


class ImagePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('image_file',)


class ImageSlideSerializer(serializers.ModelSerializer):
    IMAGE_SLIDE_RATING_CHOICES = [
        ('G', 'General'),
        ('E', 'Ecchi'),
    ]
    rating = serializers.ChoiceField(choices=IMAGE_SLIDE_RATING_CHOICES, source='get_rating_display')

    class Meta:
        model = ImageSlide
        fields = '__all__'


class ImageSlideDetailSerializer(serializers.ModelSerializer):
    IMAGE_SLIDE_RATING_CHOICES = [
        ('G', 'General'),
        ('E', 'Ecchi'),
    ]
    rating = serializers.ChoiceField(choices=IMAGE_SLIDE_RATING_CHOICES, source='get_rating_display')
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = ImageSlide
        fields = '__all__'


class ImageSlidePostSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)
    class Meta:
        model = ImageSlide
        fields = ('title', 'description', 'rating', 'tags', 'images')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'views_count', 'likes_count')

    def image_numbers_validation(self, images):
        if len(images) < 1:
            raise serializers.ValidationError('You must provide at least 2 images for image slide.')
        
        if len(images) > 12:
            raise serializers.ValidationError('You can provide at most 12 images for image slide.')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        images = validated_data.pop('images')
        self.image_numbers_validation(images)
        image_slide = ImageSlide.objects.create(**validated_data)
        for image in images:
            Image.objects.create(slide=image_slide, image_file=image)
        for tag in tags:
            image_slide.tags.add(tag)
        return image_slide


class ImageSlidePutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageSlide
        fields = ('title', 'description', 'rating', 'tags')
        read_only_fields = ('id', 'user', 'created_at', 'updated_at', 'views_count', 'likes_count')


class VideoLikeSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    avatar = serializers.ImageField(source='user.avatar')
    nickname = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = VideoLike
        fields = ('user_name', 'nickname', 'avatar', 'created_at')


class ImageSlideLikeSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    avatar = serializers.ImageField(source='user.avatar')
    nickname = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = ImageSlideLike
        fields = ('user_name', 'nickname', 'avatar', 'created_at')


class VideoCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    avatar = serializers.ImageField(source='user.avatar')
    nickname = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = VideoComment
        fields = ('id', 'content', 'user_name', 'nickname', 'avatar', 'created_at', 'parent_comment_id')


class VideoCommentPostSerializer(serializers.ModelSerializer):
    parent_comment_id = serializers.UUIDField(required=False)

    class Meta:
        model = VideoComment
        fields = ('content', 'parent_comment_id')


class VideoCommentPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoComment
        fields = ('content',)


class VideoCommentParamSerializer(serializers.Serializer):
    parent = serializers.UUIDField(required=False)


class ImageSlideCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    avatar = serializers.ImageField(source='user.avatar')
    nickname = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = ImageSlideComment
        fields = ('id', 'content', 'user_name', 'nickname', 'avatar', 'created_at', 'parent_comment_id')


class ImageSlideCommentPostSerializer(serializers.ModelSerializer):
    parent_comment_id = serializers.UUIDField(required=False)

    class Meta:
        model = ImageSlideComment
        fields = ('content', 'parent_comment_id')


class ImageSlideCommentPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageSlideComment
        fields = ('content',)


class ImageSlideCommentParamSerializer(serializers.Serializer):
    parent = serializers.UUIDField(required=False)


class UserIDParamSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()


class PlaylistSerializer(serializers.ModelSerializer):
    video_count = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ('id', 'name', 'created_at', 'video_count')

    def get_video_count(self, obj):
        return obj.videos.count()


class PlaylistNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('id', 'name', 'created_at')


class PlaylistDetailSerializer(serializers.ModelSerializer):
    video_count = serializers.SerializerMethodField()
    videos = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Playlist
        fields = ('id', 'name', 'created_at', 'video_count', 'videos')

    def get_video_count(self, obj):
        return obj.videos.count()
    

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content')


class PostDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    avatar = serializers.ImageField(source='user.avatar')
    nickname = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = PostComment
        fields = ('id', 'content', 'user_name', 'nickname', 'avatar', 'created_at', 'parent_comment_id')


class PostCommentPostSerializer(serializers.ModelSerializer):
    parent_comment_id = serializers.UUIDField(required=False)

    class Meta:
        model = PostComment
        fields = ('content', 'parent_comment_id')


class PostCommentPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ('content',)


class PostCommentParamSerializer(serializers.Serializer):
    parent = serializers.UUIDField(required=False)


class ProfileCommentSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    avatar = serializers.ImageField(source='user.avatar')
    nickname = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = ProfileComment
        fields = ('id', 'content', 'user_name', 'nickname', 'avatar', 'created_at', 'parent_comment_id')


class ProfileCommentPostSerializer(serializers.ModelSerializer):
    parent_comment_id = serializers.UUIDField(required=False)

    class Meta:
        model = ProfileComment
        fields = ('content', 'parent_comment_id')


class ProfileCommentPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileComment
        fields = ('content',)


class ProfileCommentParamSerializer(serializers.Serializer):
    parent = serializers.UUIDField(required=False)