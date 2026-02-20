from httpx import AsyncClient
from yt_dlp import YoutubeDL

from errors import VideoTooLongError

from .base import Downloader, max_resolution


class TikTokDownloader(Downloader):
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

        return info
