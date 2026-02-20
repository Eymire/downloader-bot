from httpx import AsyncClient
from PIL import Image
from yt_dlp import YoutubeDL

from errors import VideoTooLongError

from .base import Downloader, max_resolution


def crop_square_center(image_path: str):
    img = Image.open(image_path)
    width, height = img.size

    center_size = height

    left = (width - center_size) // 2
    top = 0
    right = left + center_size
    bottom = height

    cropped_img = img.crop((left, top, right, bottom))

    cropped_img.save(image_path, quality=100)


def crop_vertical_center(image_path: str):
    img = Image.open(image_path)
    width, height = img.size

    center_width = int(height * (9 / 16))

    left = (width - center_width) // 2
    top = 0
    right = left + center_width
    bottom = height

    cropped_img = img.crop((left, top, right, bottom))

    cropped_img.save(image_path, quality=100)


class ShortsDownloader(Downloader):
    @staticmethod
    async def download(
        url: str,
        video_path: str,
        thumbnail_path: str,
    ) -> dict:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': video_path,
            'quiet': True,
            'js_runtimes': {'node': {}},
            'remote_components': ['ejs:github'],
            'postprocessor_args': {
                'ffmpeg': [
                    '-c:v', 'libx265',
                    '-preset', 'ultrafast',
                    '-tag:v', 'hvc1',
                    '-c:a', 'aac',
                    '-movflags',
                    '+faststart',
                ]
            },
        }

        with YoutubeDL(ydl_opts) as ydl:  # type: ignore
            info: dict = ydl.extract_info(url, download=False)  # type: ignore

        if int(info['duration']) > 120:
            raise VideoTooLongError()

        side = 'height' if info['aspect_ratio'] >= 1 else 'width'
        ydl_opts['format'] = (
            f'bestvideo[{side}<={max_resolution}]+bestaudio/best[{side}<={max_resolution}]'
        )

        with YoutubeDL(ydl_opts) as ydl:  # type: ignore
            info: dict = ydl.extract_info(url, download=True)  # type: ignore

        async with AsyncClient() as client:
            r = await client.get(info['thumbnail'])

            with open(thumbnail_path, 'wb') as f:
                f.write(r.content)

        if info['aspect_ratio'] < 1:
            crop_vertical_center(thumbnail_path)
        else:
            crop_square_center(thumbnail_path)

        return info
