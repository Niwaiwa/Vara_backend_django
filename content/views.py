from json import JSONDecodeError
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import views, status
from vara_backend.settings import CONTENT_PAGE_SIZE

from .models import Video, Tag
from .serializers import VideoSerializer, VideoPostSerializer, VideoPutSerializer, TagSerializer
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
