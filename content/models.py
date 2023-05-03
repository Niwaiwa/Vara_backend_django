import uuid
from django.db import models
from django.utils.text import slugify   
from vara_backend.settings import AUTH_USER_MODEL as User
from utils.commons import UniqueFilename

video_upload_path = UniqueFilename('videos/')


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
    VIDEO_RATING_CHOICES = [
        ('G', 'General'),
        ('E', 'Ecchi'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to=video_upload_path)
    video_url = models.URLField(null=True, blank=True)
    rating = models.CharField(choices=VIDEO_RATING_CHOICES, max_length=2, default='G')
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
