import uuid
from django.db import models
from django.utils.text import slugify   
from vara_backend.settings import AUTH_USER_MODEL as User
from utils.commons import UniqueFilename

video_upload_path = UniqueFilename('videos/')
image_upload_path = UniqueFilename('images/')


class Tag(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Video(models.Model):
    RATING_CHOICES = [
        ('G', 'General'),
        ('E', 'Ecchi'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to=video_upload_path)
    video_url = models.URLField(null=True, blank=True)
    rating = models.CharField(choices=RATING_CHOICES, max_length=2, default='G')
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')
    tags = models.ManyToManyField('Tag', related_name='taged_videos', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def increment_views_count(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def increment_likes_count(self):
        self.likes_count += 1
        self.save(update_fields=['likes_count'])

    def decrement_likes_count(self):
        self.likes_count -= 1
        self.save(update_fields=['likes_count'])

 
class ImageSlide(models.Model):
    RATING_CHOICES = [
        ('G', 'General'),
        ('E', 'Ecchi'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    rating = models.CharField(choices=RATING_CHOICES, max_length=2, default='G')
    views_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='image_slides')
    tags = models.ManyToManyField('Tag', related_name='taged_image_slides', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def increment_views_count(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])

    def increment_likes_count(self):
        self.likes_count += 1
        self.save(update_fields=['likes_count'])

    def decrement_likes_count(self):
        self.likes_count -= 1
        self.save(update_fields=['likes_count'])


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slide = models.ForeignKey(ImageSlide, on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(upload_to=image_upload_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class ImageSlideLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slide = models.ForeignKey(ImageSlide, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='image_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['slide', 'user'], name='unique_slide_like')
        ]


class VideoLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(fields=['video', 'user'], name='unique_video_like')
        ]


class VideoComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='replies', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']


class ImageSlideComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slide = models.ForeignKey(ImageSlide, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='image_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='replies', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']


class Playlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='playlists', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    videos = models.ManyToManyField(Video, related_name='playlists', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PostComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='post_comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='replies', null=True, blank=True)


class ProfileComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='profile_comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_comment = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='replies', null=True, blank=True)
