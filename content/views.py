from json import JSONDecodeError
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import views, status
from vara_backend.settings import CONTENT_PAGE_SIZE, SMALL_PAGE_SIZE


from .models import Video, Tag, ImageSlide, Image, VideoLike, ImageSlideLike, Playlist, Post, PostComment \
    , Forum, ForumThread, ForumPost, ProfileComment, VideoComment, ImageSlideComment
from .serializers import VideoSerializer, VideoPostSerializer, VideoPutSerializer, TagSerializer \
    , ImageSlideSerializer, ImageSlidePostSerializer, ImageSlidePutSerializer, ImageSerializer \
    , ImagePostSerializer, ImageSlideDetailSerializer, ImageSlideLikeSerializer, VideoLikeSerializer \
    , ImageSlideCommentSerializer, VideoCommentSerializer, VideoCommentPostSerializer \
    , ImageSlideCommentPostSerializer, VideoCommentParamSerializer, ImageSlideCommentParamSerializer \
    , ImageSlideCommentPutSerializer, VideoCommentPutSerializer, PlaylistSerializer, PlaylistNameSerializer \
    , PlaylistDetailSerializer, UserIDParamSerializer, PostSerializer, PostEditSerializer, PostDetailSerializer \
    , PostCommentSerializer, PostCommentPostSerializer, PostCommentPutSerializer, PostCommentParamSerializer \
    , ProfileCommentSerializer, ProfileCommentPostSerializer, ProfileCommentPutSerializer, ProfileCommentParamSerializer \
    , ForumSerializer, ForumPostMethodSerializer, ForumThreadSerializer, ForumThreadPostSerializer \
    , ForumPostSerializer, ForumPostPostSerializer, ForumThreadPutSerializer, ForumPostPutSerializer
from core.models import User, Notification
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
        serializer = ImageSlideLikeSerializer(page_obj, many=True)
        return Response(serializer.data)


    def post(self, request, pk):
        slide = get_object_or_404(ImageSlide, pk=pk)
        images_like = ImageSlideLike.objects.filter(slide=slide, user=request.user)
        if images_like:
            return Response({"result": 'error', 'message': 'You are already liked this images'}, status=status.HTTP_400_BAD_REQUEST)
        images_like = ImageSlideLike.objects.create(slide=slide, user=request.user)
        slide.increment_likes_count()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ImageSlideUnLikeAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def post(self, request, pk):
        slide = get_object_or_404(ImageSlide, pk=pk)
        images_like = ImageSlideLike.objects.filter(slide=slide, user=request.user)
        if not images_like:
            return Response({"result": 'error', 'message': 'You are not liked this images'}, status=status.HTTP_400_BAD_REQUEST)
        images_like.delete()
        slide.decrement_likes_count()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VideoCommentListCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request, video_id):
        parent_comment_id = None
        query = VideoCommentParamSerializer(data=request.query_params)
        if query.is_valid():
            parent_comment_id = query.validated_data.get('parent')

        video = get_object_or_404(Video, pk=video_id)
        if parent_comment_id:
            video_comment = get_object_or_404(VideoComment, pk=parent_comment_id)
            video_comments = video.comments.filter(parent_comment=parent_comment_id).order_by('created_at')
        else:
            video_comments = video.comments.filter(parent_comment=None).order_by('created_at')

        page = request.GET.get('page', 1)
        paginator = Paginator(video_comments, SMALL_PAGE_SIZE)
        page_obj = paginator.get_page(page)
        serializer = VideoCommentSerializer(page_obj, many=True)
        return Response(serializer.data)

    def post(self, request, video_id):
        try:
            video = get_object_or_404(Video, pk=video_id)
            data = JSONParser().parse(request)
            serializer = VideoCommentPostSerializer(data=data)
            if serializer.is_valid():
                parent_comment_id = serializer.validated_data.get('parent_comment_id')
                if parent_comment_id:
                    video_comment = video.comments.filter(pk=parent_comment_id).first()
                    if video_comment:
                        serializer.save(video=video, user=request.user, parent_comment=video_comment)
                        if video.user != request.user:
                            notification = Notification.objects.create(
                                user=video.user, message=f'{request.user.nickname} replied to your comment', url=f'/video/{video.id}')
                        response_serializer = VideoCommentSerializer(serializer.instance)
                        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"result": "error", "message": "Invalid parent comment id"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer.save(video=video, user=request.user)
                    if video.user != request.user:
                        notification = Notification.objects.create(
                            user=video.user, message=f'{request.user.nickname} commented on your video', url=f'/video/{video.id}')
                    response_serializer = VideoCommentSerializer(serializer.instance)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return Response({"result": "error", "message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        

class VideoCommentDetailAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def put(self, request, video_id, comment_id):
        try:
            video = get_object_or_404(Video, pk=video_id)
            data = JSONParser().parse(request)
            serializer = VideoCommentPutSerializer(data=data)
            if serializer.is_valid():
                video_comment = video.comments.filter(user=request.user, pk=comment_id).first()
                if video_comment:
                    video_comment.content = serializer.validated_data.get('content')
                    video_comment.save()
                    response_serializer = VideoCommentSerializer(video_comment)
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"result": "error", "message": "Invalid comment id"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return Response({"result": "error", "message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, video_id, comment_id):
        try:
            video = get_object_or_404(Video, pk=video_id)
            video_comment = video.comments.filter(user=request.user, pk=comment_id).first()
            if video_comment:
                video_comment.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:    
                return Response({"result": "error", "message": "Invalid comment id"}, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return Response({"result": "error", "message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class ImageSlideCommentListCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request, images_id):
        parent_comment_id = None
        query = ImageSlideCommentParamSerializer(data=request.query_params)
        if query.is_valid():
            parent_comment_id = query.validated_data.get('parent')

        slide = get_object_or_404(ImageSlide, pk=images_id)
        if parent_comment_id:
            image_comment = get_object_or_404(ImageSlideComment, pk=parent_comment_id)
            image_comments = slide.comments.filter(parent_comment=parent_comment_id).order_by('created_at')
        else:
            image_comments = slide.comments.filter(parent_comment=None).order_by('created_at')

        page = request.GET.get('page', 1)
        paginator = Paginator(image_comments, SMALL_PAGE_SIZE)
        page_obj = paginator.get_page(page)
        serializer = ImageSlideCommentSerializer(page_obj, many=True)
        return Response(serializer.data)

    def post(self, request, images_id):
        try:
            slide = get_object_or_404(ImageSlide, pk=images_id)
            data = JSONParser().parse(request)
            serializer = ImageSlideCommentPostSerializer(data=data)
            if serializer.is_valid():
                parent_comment_id = serializer.validated_data.get('parent_comment_id')
                if parent_comment_id:
                    image_comment = slide.comments.filter(pk=parent_comment_id).first()
                    if image_comment:
                        serializer.save(slide=slide, user=request.user, parent_comment=image_comment)
                        if slide.user != request.user:
                            notification = Notification.objects.create(
                                user=slide.user, message=f'{request.user.nickname} replied to your comment', url=f'/images/{slide.id}')
                        response_serializer = ImageSlideCommentSerializer(serializer.instance)
                        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"result": "error", "message": "Invalid parent comment id"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer.save(slide=slide, user=request.user)
                    if slide.user != request.user:
                        notification = Notification.objects.create(
                            user=slide.user, message=f'{request.user.nickname} commented on your images', url=f'/images/{slide.id}')
                    response_serializer = ImageSlideCommentSerializer(serializer.instance)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return Response({"result": "error", "message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        

class ImageSlideCommentDetailAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def put(self, request, images_id, comment_id):
        try:
            slide = get_object_or_404(ImageSlide, pk=images_id)
            data = JSONParser().parse(request)
            serializer = ImageSlideCommentPutSerializer(data=data)
            if serializer.is_valid():
                image_comment = slide.comments.filter(user=request.user, pk=comment_id).first()
                if image_comment:
                    image_comment.content = serializer.validated_data.get('content')
                    image_comment.save()
                    response_serializer = ImageSlideCommentSerializer(image_comment)
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"result": "error", "message": "Invalid comment id"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return Response({"result": "error", "message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, images_id, comment_id):
        try:
            slide = get_object_or_404(ImageSlide, pk=images_id)
            image_comment = slide.comments.filter(user=request.user, pk=comment_id).first()
            if image_comment:
                image_comment.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:    
                return Response({"result": "error", "message": "Invalid comment id"}, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return Response({"result": "error", "message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class PlaylistAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def paginate_queryset(self, queryset, page_size):
        paginator = Paginator(queryset, page_size)
        page = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page)
        return page_obj

    def get(self, request):
        order_by = '-created_at'
        if request.user.is_authenticated:
            playlists = Playlist.objects.filter(user=request.user).order_by(order_by)
            page_obj = self.paginate_queryset(playlists, CONTENT_PAGE_SIZE)
            if request.query_params.get('type') == 'name':
                serializer = PlaylistNameSerializer(page_obj, many=True)
            else:
                serializer = PlaylistSerializer(page_obj, many=True)
            return Response(serializer.data)
        else:
            query = UserIDParamSerializer(data=request.query_params)
            if query.is_valid():
                user_id = query.validated_data.get('user_id')
                if user_id:
                    user = get_object_or_404(User, pk=user_id)
                    playlists = Playlist.objects.filter(user=user).order_by(order_by)
                    page_obj = self.paginate_queryset(playlists, CONTENT_PAGE_SIZE)
                    serializer = PlaylistSerializer(page_obj, many=True)
                    return Response(serializer.data)
            return Response([])

    def post(self, request):
        try:
            data = JSONParser().parse(request)
            name = data.get('name')
            if not name:
                return Response({"result": 'error', 'message': 'name is required'}, status=status.HTTP_400_BAD_REQUEST)
            playlist = Playlist.objects.filter(user=request.user, name=name)
            if playlist:
                return Response({"result": 'error', 'message': 'You already have a playlist with this name'}, status=status.HTTP_400_BAD_REQUEST)
            playlist = Playlist.objects.create(user=request.user, name=name)
            return Response({"result": 'success', 'message': f'You created a playlist {playlist.name}!'}, status=status.HTTP_200_OK)
        except JSONDecodeError:
            return JsonResponse({"result": 'error', 'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)


class PlaylistDetailAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, pk=playlist_id, user=request.user)
        serializer = PlaylistDetailSerializer(playlist)
        return Response(serializer.data)

    def delete(self, request, playlist_id):
        playlist = get_object_or_404(Playlist, pk=playlist_id, user=request.user)
        playlist.delete()
        return Response({"result": 'success', 'message': f'You deleted the playlist {playlist.name}!'}, status=status.HTTP_200_OK)


class PlaylistVideoAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, playlist_id, video_id):
        playlist = get_object_or_404(Playlist, pk=playlist_id, user=request.user)
        video = get_object_or_404(Video, pk=video_id)
        playlist_video = playlist.videos.filter(pk=video_id)
        if playlist_video:
            return Response({"result": 'error', 'message': f'You already have the video {video.title} in the playlist {playlist.name}!'}, status=status.HTTP_400_BAD_REQUEST)
        playlist.videos.add(video)
        return Response({"result": 'success', 'message': f'You added the video {video.title} to the playlist {playlist.name}!'}, status=status.HTTP_200_OK)

    def delete(self, request, playlist_id, video_id):
        playlist = get_object_or_404(Playlist, pk=playlist_id, user=request.user)
        video = get_object_or_404(Video, pk=video_id)
        playlist_video = playlist.videos.filter(pk=video_id)
        if not playlist_video:
            return Response({"result": 'error', 'message': f'You don\'t have the video {video.title} in the playlist {playlist.name}!'}, status=status.HTTP_400_BAD_REQUEST)
        playlist.videos.remove(video)
        return Response({"result": 'success', 'message': f'You removed the video {video.title} from the playlist {playlist.name}!'}, status=status.HTTP_200_OK)


class PostAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def paginate_queryset(self, queryset, page_size):
        paginator = Paginator(queryset, page_size)
        page = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page)
        return page_obj

    def get(self, request):
        order_by = '-created_at'
        if request.user.is_authenticated:
            posts = Post.objects.filter(user=request.user).order_by(order_by)
            page_obj = self.paginate_queryset(posts, CONTENT_PAGE_SIZE)
            serializer = PostSerializer(page_obj, many=True)
            return Response(serializer.data)
        else:
            query = UserIDParamSerializer(data=request.query_params)
            if query.is_valid():
                user_id = query.validated_data.get('user_id')
                if user_id:
                    user = get_object_or_404(User, pk=user_id)
                    posts = Post.objects.filter(user=user).order_by(order_by)
                    page_obj = self.paginate_queryset(posts, CONTENT_PAGE_SIZE)
                    serializer = PostSerializer(page_obj, many=True)
                    return Response(serializer.data)
            return Response([])

    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = PostEditSerializer(data=data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                serializer = PostDetailSerializer(serializer.instance)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"result": 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": 'error', 'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        

class PostDetailAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)
    
    def put(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id, user=request.user)
        try:
            data = JSONParser().parse(request)
            serializer = PostEditSerializer(post, data=data)
            if serializer.is_valid():
                serializer.save(user=request.user)
                serializer = PostDetailSerializer(serializer.instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"result": 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": 'error', 'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        post = get_object_or_404(Post, pk=post_id, user=request.user)
        post.delete()
        return Response({"result": 'success', 'message': f'You deleted the post!'}, status=status.HTTP_200_OK)
    

class PostCommentListCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request, post_id):
        parent_comment_id = None
        query = PostCommentParamSerializer(data=request.query_params)
        if query.is_valid():
            parent_comment_id = query.validated_data.get('parent')

        post = get_object_or_404(Post, pk=post_id)
        if parent_comment_id:
            post_comment = get_object_or_404(PostComment, pk=parent_comment_id, post=post)
            post_comments = post.comments.filter(parent_comment=parent_comment_id).order_by('created_at')
        else:
            post_comments = post.comments.filter(parent_comment=None).order_by('created_at')

        page = request.GET.get('page', 1)
        paginator = Paginator(post_comments, SMALL_PAGE_SIZE)
        page_obj = paginator.get_page(page)
        serializer = PostCommentSerializer(page_obj, many=True)
        return Response(serializer.data)

    def post(self, request, post_id):
        try:
            post = get_object_or_404(Post, pk=post_id)
            data = JSONParser().parse(request)
            serializer = PostCommentPostSerializer(data=data)
            if serializer.is_valid():
                parent_comment_id = serializer.validated_data.get('parent_comment_id')
                if parent_comment_id:
                    post_comment = post.comments.filter(pk=parent_comment_id).first()
                    if post_comment:
                        serializer.save(post=post, user=request.user, parent_comment=post_comment)
                        if post.user != request.user:
                            notification = Notification.objects.create(
                                user=post.user, message=f'{request.user.nickname} replied to your comment', url=f'/post/{post.id}')
                        response_serializer = PostCommentSerializer(serializer.instance)
                        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"result": "error", "message": "Invalid parent comment id"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer.save(post=post, user=request.user)
                    if post.user != request.user:
                        notification = Notification.objects.create(
                            user=post.user, message=f'{request.user.nickname} commented on your post', url=f'/post/{post.id}')
                    response_serializer = PostCommentSerializer(serializer.instance)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return Response({"result": "error", "message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        

class PostCommentDetailAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def put(self, request, post_id, comment_id):
        try:
            post = get_object_or_404(Post, pk=post_id)
            data = JSONParser().parse(request)
            serializer = PostCommentPutSerializer(data=data)
            if serializer.is_valid():
                post_comment = post.comments.filter(user=request.user, pk=comment_id).first()
                if post_comment:
                    post_comment.content = serializer.validated_data.get('content')
                    post_comment.save()
                    response_serializer = PostCommentSerializer(post_comment)
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"result": "error", "message": "Invalid comment id"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return Response({"result": "error", "message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id, comment_id):
        try:
            post = get_object_or_404(Post, pk=post_id)
            post_comment = post.comments.filter(user=request.user, pk=comment_id).first()
            if post_comment:
                post_comment.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"result": "error", "message": "Invalid comment id"}, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return Response({"result": "error", "message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileCommentListCreateAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request, user_id):
        parent_comment_id = None
        query = ProfileCommentParamSerializer(data=request.query_params)
        if query.is_valid():
            parent_comment_id = query.validated_data.get('parent')

        user = get_object_or_404(User, pk=user_id)
        if parent_comment_id:
            profile_comment = get_object_or_404(ProfileComment, pk=parent_comment_id, profile=user)
            profile_comments = user.profile_comments.filter(parent_comment=parent_comment_id).order_by('created_at')
        else:
            profile_comments = user.profile_comments.filter(parent_comment=None).order_by('created_at')

        page = request.GET.get('page', 1)
        paginator = Paginator(profile_comments, SMALL_PAGE_SIZE)
        page_obj = paginator.get_page(page)
        serializer = ProfileCommentSerializer(page_obj, many=True)
        return Response(serializer.data)

    def post(self, request, user_id):
        try:
            user = get_object_or_404(User, pk=user_id)
            data = JSONParser().parse(request)
            serializer = ProfileCommentPostSerializer(data=data)
            if serializer.is_valid():
                parent_comment_id = serializer.validated_data.get('parent_comment_id')
                if parent_comment_id:
                    profile_comment = user.profile_comments.filter(pk=parent_comment_id).first()
                    if profile_comment:
                        serializer.save(profile=user, user=request.user, parent_comment=profile_comment)
                        if user != request.user:
                            notification = Notification.objects.create(
                                user=user, message=f'{request.user.nickname} replied to your comment', url=f'/profile/{user.username}')
                        response_serializer = ProfileCommentSerializer(serializer.instance)
                        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"result": "error", "message": "Invalid parent comment id"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer.save(profile=user, user=request.user)
                    if user != request.user:
                        notification = Notification.objects.create(
                            user=user, message=f'{request.user.nickname} commented on your profile', url=f'/profile/{user.username}')
                    response_serializer = ProfileCommentSerializer(serializer.instance)
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return Response({"result": "error", "message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileCommentDetailAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def put(self, request, user_id, comment_id):
        try:
            user = get_object_or_404(User, pk=user_id)
            data = JSONParser().parse(request)
            serializer = ProfileCommentPutSerializer(data=data)
            if serializer.is_valid():
                profile_comment = user.profile_comments.filter(user=request.user, pk=comment_id).first()
                if profile_comment:
                    profile_comment.content = serializer.validated_data.get('content')
                    profile_comment.save()
                    response_serializer = ProfileCommentSerializer(profile_comment)
                    return Response(response_serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"result": "error", "message": "Invalid comment id"}, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return Response({"result": "error", "message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, comment_id):
        try:
            user = get_object_or_404(User, pk=user_id)
            profile_comment = user.profile_comments.filter(user=request.user, pk=comment_id).first()
            if profile_comment:
                profile_comment.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({"result": "error", "message": "Invalid comment id"}, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return Response({"result": "error", "message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
        

class ForumAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request):
        forums = Forum.objects.filter().order_by('category', 'title')
        serializer = ForumSerializer(forums, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            if request.user != User.objects.get(is_superuser=True):
                return Response({"result": 'error', 'message': 'You are not admin'}, status=status.HTTP_400_BAD_REQUEST)

            data = JSONParser().parse(request)
            serializer = ForumPostMethodSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"result": 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": 'error', 'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        

class ForumDetailAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, forum_id):
        if request.user != User.objects.get(is_superuser=True):
            return Response({"result": 'error', 'message': 'You are not admin'}, status=status.HTTP_400_BAD_REQUEST)

        forum = get_object_or_404(Forum, pk=forum_id)
        forum.delete()
        return Response({"result": 'success', 'message': f'You deleted the forum!'}, status=status.HTTP_200_OK)
    

class ForumThreadAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def pageinate_queryset(self, queryset, page_size):
        paginator = Paginator(queryset, page_size)
        page = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page)
        return page_obj

    def get(self, request, forum_id):
        forum = get_object_or_404(Forum, pk=forum_id)
        threads = forum.forum_threads.filter().order_by('-created_at')
        page_obj = self.pageinate_queryset(threads, CONTENT_PAGE_SIZE)
        serializer = ForumThreadSerializer(page_obj, many=True)
        return Response(serializer.data)

    def post(self, request, forum_id):
        try:
            forum = get_object_or_404(Forum, pk=forum_id)
            data = JSONParser().parse(request)
            thread_serializer = ForumThreadPostSerializer(data=data)
            if thread_serializer.is_valid():
                thread_validate_data = thread_serializer.validated_data
                content = thread_validate_data.pop('content', None)
                thread = ForumThread.objects.create(user=request.user, forum=forum, **thread_validate_data)
                post = ForumPost.objects.create(user=request.user, thread=thread, content=content)

                forum.increment_threads_count()
                forum.increment_posts_count()
                thread.increment_posts_count()
                thread_serializer = ForumThreadSerializer(thread)
                return Response(thread_serializer.data, status=status.HTTP_201_CREATED)
            return Response({"result": 'error', 'message': thread_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": 'error', 'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        

class ForumThreadDetailAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def put(self, request, forum_id, thread_id):
        try:
            forum = get_object_or_404(Forum, pk=forum_id)
            data = JSONParser().parse(request)
            if request.user == User.objects.get(is_superuser=True):
                thread = get_object_or_404(ForumThread, pk=thread_id)
                serializer = ForumThreadPutSerializer(thread, data=data)
            else:
                thread = get_object_or_404(ForumThread, pk=thread_id, user=request.user)
                user_data = {
                    'title': data.get('title'),
                    'description': data.get('description'),
                }
                serializer = ForumThreadPutSerializer(thread, data=user_data)

            if serializer.is_valid():
                serializer.save(user=request.user)
                serializer = ForumThreadSerializer(serializer.instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"result": 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": 'error', 'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, forum_id, thread_id):
        forum = get_object_or_404(Forum, pk=forum_id)
        if request.user == User.objects.get(is_superuser=True):
            thread = get_object_or_404(ForumThread, pk=thread_id)
        else:
            thread = get_object_or_404(ForumThread, pk=thread_id, user=request.user)
        forum.decrement_threads_count()
        forum.posts_count -= thread.posts_count
        forum.save()
        thread.delete()
        return Response({"result": 'success', 'message': f'You deleted the thread!'}, status=status.HTTP_200_OK)
    

class ForumPostAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def pageinate_queryset(self, queryset, page_size):
        paginator = Paginator(queryset, page_size)
        page = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page)
        return page_obj

    def get(self, request, forum_id, thread_id):
        forum = get_object_or_404(Forum, pk=forum_id)
        thread = get_object_or_404(ForumThread, pk=thread_id)
        posts = thread.thread_posts.filter().order_by('created_at')
        page_obj = self.pageinate_queryset(posts, SMALL_PAGE_SIZE)
        data = {
            'thread': ForumThreadSerializer(thread).data,
            'posts': ForumPostSerializer(page_obj, many=True).data,
        }
        thread.increment_views_count()
        return Response(data)

    def post(self, request, forum_id, thread_id):
        try:
            forum = get_object_or_404(Forum, pk=forum_id)
            thread = get_object_or_404(ForumThread, pk=thread_id)
            data = JSONParser().parse(request)
            serializer = ForumPostPostSerializer(data=data)
            if serializer.is_valid():
                serializer.save(user=request.user, thread=thread)
                forum.increment_posts_count()
                thread.increment_posts_count()
                serializer = ForumPostSerializer(serializer.instance)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response({"result": 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": 'error', 'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)
        

class ForumPostDetailAPIView(views.APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def put(self, request, forum_id, thread_id, post_id):
        try:
            forum = get_object_or_404(Forum, pk=forum_id)
            thread = get_object_or_404(ForumThread, pk=thread_id)
            data = JSONParser().parse(request)
            if request.user == User.objects.get(is_superuser=True):
                post = get_object_or_404(ForumPost, pk=post_id)
                serializer = ForumPostPutSerializer(post, data=data)
            else:
                post = get_object_or_404(ForumPost, pk=post_id, user=request.user)
                user_data = {
                    'content': data.get('content'),
                }
                serializer = ForumPostPutSerializer(post, data=user_data)

            if serializer.is_valid():
                serializer.save(user=request.user)
                serializer = ForumPostSerializer(serializer.instance)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"result": 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": 'error', 'message': 'Invalid JSON'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, forum_id, thread_id, post_id):
        forum = get_object_or_404(Forum, pk=forum_id)
        thread = get_object_or_404(ForumThread, pk=thread_id)
        if request.user == User.objects.get(is_superuser=True):
            post = get_object_or_404(ForumPost, pk=post_id)
        else:
            post = get_object_or_404(ForumPost, pk=post_id, user=request.user)
        post.delete()
        forum.decrement_posts_count()
        thread.decrement_posts_count()
        return Response({"result": 'success', 'message': f'You deleted the post!'}, status=status.HTTP_200_OK)