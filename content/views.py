from json import JSONDecodeError
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import views, status
from vara_backend.settings import CONTENT_PAGE_SIZE, SMALL_PAGE_SIZE

from .models import Video, Tag, ImageSlide, Image, VideoLike, ImageLike
from .serializers import VideoSerializer, VideoPostSerializer, VideoPutSerializer, TagSerializer \
    , ImageSlideSerializer, ImageSlidePostSerializer, ImageSlidePutSerializer, ImageSerializer \
    , ImagePostSerializer, ImageSlideDetailSerializer, ImageLikeSerializer, VideoLikeSerializer
from utils.commons import ReadOnly

sort_map = {
    'date': '-created_at',
    'views': '-views_count',
    'likes': '-likes_count',
}


class VideoListCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request):
        page = request.GET.get('page', 1)
        rating = request.GET.get('rating', None)
        tag = request.GET.get('tag', '')
        sort = request.GET.get('sort', 'date')
        order_by = sort_map.get(sort, '-created_at')

        if rating:
            videos = Video.objects.filter(rating=rating).order_by(order_by)
        else:
            videos = Video.objects.all().order_by(order_by)

        if tag:
            videos = videos.filter(tags__name=tag)

        paginator = Paginator(videos, CONTENT_PAGE_SIZE)
        page_obj = paginator.get_page(page)
        serializer = VideoSerializer(page_obj, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = VideoPostSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.tags.add(*request.data.get('tags'))
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoDetailAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    # parser_classes = [MultiPartParser, FormParser]

    def get(self, request, pk): 
        video = get_object_or_404(Video, pk=pk)
        video.increment_views_count()
        serializer = VideoSerializer(video)
        return Response(serializer.data)

    def put(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        serializer = VideoPutSerializer(video, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def paginate_queryset(self, queryset, page_size):
        paginator = Paginator(queryset, page_size)
        page = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page)
        return page_obj

    def get(self, request):
        filter = request.GET.get('filter', '')
        tag_name = request.GET.get('tag', '')

        tags = Tag.objects.all().order_by('name')
        if filter:
            tags = tags.filter(name__startswith=filter)
            page_obj = self.paginate_queryset(tags, CONTENT_PAGE_SIZE)
            serializer = TagSerializer(page_obj, many=True)
            return Response(serializer.data)
       
        if tag_name:
            tags = tags.filter(name__icontains=tag_name)

        page_obj = self.paginate_queryset(tags, CONTENT_PAGE_SIZE)
        serializer = TagSerializer(page_obj, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = TagSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": 'error', 'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        try:
            data = JSONParser().parse(request)
            tag = get_object_or_404(Tag, pk=data['name'])
            tag.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except JSONDecodeError:
            return JsonResponse({"result": 'error', 'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)


class ImageSlideListCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request):
        page = request.GET.get('page', 1)
        rating = request.GET.get('rating', None)
        tag = request.GET.get('tag', '')
        sort = request.GET.get('sort', 'date')
        order_by = sort_map.get(sort, '-created_at')

        if rating:
            imageslides = ImageSlide.objects.filter(rating=rating).order_by(order_by)
        else:
            imageslides = ImageSlide.objects.all().order_by(order_by)

        if tag:
            imageslides = imageslides.filter(tags__name=tag)

        paginator = Paginator(imageslides, CONTENT_PAGE_SIZE)
        page_obj = paginator.get_page(page)
        serializer = ImageSlideSerializer(page_obj, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ImageSlidePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            serializer = ImageSlideDetailSerializer(serializer.instance, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageSlideDetailAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    # parser_classes = [MultiPartParser, FormParser]

    def get(self, request, pk):
        imageslide = get_object_or_404(ImageSlide, pk=pk)
        imageslide.increment_views_count()
        serializer = ImageSlideDetailSerializer(imageslide, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        imageslide = get_object_or_404(ImageSlide, pk=pk)
        serializer = ImageSlidePutSerializer(imageslide, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_serializer = ImageSlideDetailSerializer(serializer.instance, context={'request': request})
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        imageslide = get_object_or_404(ImageSlide, pk=pk)
        imageslide.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ImageListCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request, images_id):
        image_slide = get_object_or_404(ImageSlide, pk=images_id)
        page = request.GET.get('page', 1)

        image_list = Image.objects.all().order_by('-created_at')
        paginator = Paginator(image_list, CONTENT_PAGE_SIZE)
        page_obj = paginator.get_page(page)
        serializer = ImageSerializer(page_obj, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request, images_id):
        image_slide = get_object_or_404(ImageSlide, pk=images_id)
        serializer = ImagePostSerializer(data=request.data)
        if serializer.is_valid():
            # serializer.tags.add(*request.data.get('tags'))
            serializer.save(slide=image_slide)
            response_serializer = ImageSerializer(serializer.instance, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageDetailAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    # parser_classes = [MultiPartParser, FormParser]

    def get(self, request, images_id, pk):
        image_slide = get_object_or_404(ImageSlide, pk=images_id)
        image = get_object_or_404(Image, pk=pk)
        serializer = ImageSerializer(image, context={'request': request})
        return Response(serializer.data)

    def delete(self, request, images_id, pk):
        image = get_object_or_404(Image, pk=pk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VideoLikeAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        video_likes = video.likes.all().order_by('-created_at')

        page = request.GET.get('page', 1)
        paginator = Paginator(video_likes, SMALL_PAGE_SIZE)
        page_obj = paginator.get_page(page)
        serializer = VideoLikeSerializer(page_obj, many=True)
        return Response(serializer.data)


    def post(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        video_like = VideoLike.objects.filter(video=video, user=request.user)
        if video_like:
            return Response({"result": 'error', 'message': 'You are already liked this video'}, status=status.HTTP_400_BAD_REQUEST)
        video_like = VideoLike.objects.create(video=video, user=request.user)
        video.increment_likes_count()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class VideoUnlikeAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def post(self, request, pk):
        video = get_object_or_404(Video, pk=pk)
        video_like = VideoLike.objects.filter(video=video, user=request.user)
        if not video_like:
            return Response({"result": 'error', 'message': 'You are not liked this video'}, status=status.HTTP_400_BAD_REQUEST)
        video_like.delete()
        video.decrement_likes_count()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageSlideLikeAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request, pk):
        image = get_object_or_404(ImageSlide, pk=pk)
        image_likes = image.likes.all().order_by('-created_at')

        page = request.GET.get('page', 1)
        paginator = Paginator(image_likes, SMALL_PAGE_SIZE)
        page_obj = paginator.get_page(page)
        serializer = ImageLikeSerializer(page_obj, many=True)
        return Response(serializer.data)


    def post(self, request, pk):
        slide = get_object_or_404(ImageSlide, pk=pk)
        images_like = ImageLike.objects.filter(slide=slide, user=request.user)
        if images_like:
            return Response({"result": 'error', 'message': 'You are already liked this images'}, status=status.HTTP_400_BAD_REQUEST)
        images_like = ImageLike.objects.create(slide=slide, user=request.user)
        slide.increment_likes_count()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageSlideUnLikeAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def post(self, request, pk):
        slide = get_object_or_404(ImageSlide, pk=pk)
        images_like = ImageLike.objects.filter(slide=slide, user=request.user)
        if not images_like:
            return Response({"result": 'error', 'message': 'You are not liked this images'}, status=status.HTTP_400_BAD_REQUEST)
        images_like.delete()
        slide.decrement_likes_count()
        return Response(status=status.HTTP_204_NO_CONTENT)
