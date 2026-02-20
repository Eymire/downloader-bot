from abc import ABC, abstractmethod


max_resolution = 1080


class Downloader(ABC):
    @staticmethod
    @abstractmethod
    async def download(
        url: str,
        video_path: str,
        thumbnail_path: str,
    ) -> dict: ...
