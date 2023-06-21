import math
import os
from rest_framework_simplejwt.tokens import RefreshToken
from moviepy.editor import VideoFileClip
from PIL import Image
from vara_backend.settings import MEDIA_ROOT


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def generate_video_thumbnails(video_path, file_id, num_thumbnails: int = 12):
    origin_path = os.path.join(MEDIA_ROOT, video_path)
    clip = VideoFileClip(origin_path)
    duration = clip.duration
    interval = duration / num_thumbnails
    thumbnails = []

    thumbnail_relate_path = os.path.join(MEDIA_ROOT, f"videos/thumbnails/{file_id}")
    os.makedirs(thumbnail_relate_path, exist_ok=True)
    for i in range(num_thumbnails):
        time = i * interval
        thumbnail_path = os.path.join(thumbnail_relate_path, f"thumbnails_{i}.jpg")
        thumbnail = clip.save_frame(thumbnail_path, time)
        thumbnails.append(thumbnail)

    clip.close()

    return True


def generate_image_thumbnail(image_path, slide_id, file_id, size=(720, 640)):
    origin_path = os.path.join(MEDIA_ROOT, image_path)
    image = Image.open(origin_path)

    thumbnail_relate_path = os.path.join(MEDIA_ROOT, f"images/thumbnails/{slide_id}")
    os.makedirs(thumbnail_relate_path, exist_ok=True)
    thumbnail_path = os.path.join(thumbnail_relate_path, f"{file_id}.jpg")

    # アスペクト比を維持しながらサイズ変更
    width, height = image.size
    target_width, target_height = size
    aspect_ratio = min(target_width / width, target_height / height)
    resized_width = math.floor(width * aspect_ratio)
    resized_height = math.floor(height * aspect_ratio)
    resized_image = image.resize((resized_width, resized_height), Image.ANTIALIAS)

    # 黒い背景で指定したサイズに埋め込む
    background = Image.new('RGB', size, (0, 0, 0))
    offset = ((target_width - resized_width) // 2, (target_height - resized_height) // 2)
    background.paste(resized_image, offset)

    # サムネイルを保存
    background.save(thumbnail_path)

    image.close()

    return True
