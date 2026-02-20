import os.path

from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import FSInputFile, Message
from pydantic import HttpUrl, ValidationError

from downloader.reels import ReelsDownloader
from downloader.shorts import ShortsDownloader
from downloader.tiktok import TikTokDownloader
from errors import VideoTooLongError


router = Router()


@router.message(Command('download'))
async def cmd_download(message: Message, command: CommandObject) -> None:
    if command.args is None or len(command.args.split(' ')) < 1:
        await message.answer('Please provide a URL to download.')
        return

    try:
        url = HttpUrl(command.args.split(' ')[0])
    except ValidationError:
        await message.answer('Invalid URL provided.')
        return

    if url.host.endswith('tiktok.com'):  # type: ignore
        downloader = TikTokDownloader
    elif url.host.endswith('youtube.com') or url.path.startswith('/shorts/'):  # type: ignore
        downloader = ShortsDownloader
    elif url.host.endswith('instagram.com') and url.path.startswith('/reel/'):  # type: ignore
        downloader = ReelsDownloader
    else:
        await message.answer('Unsupported URL provided.')
        return

    video_file_name = f'{message.chat.id}_{message.message_id}.mp4'
    video_file_path = os.path.join('./videos', video_file_name)
    thumbnail_file_name = f'{message.chat.id}_{message.message_id}_thumbnail.jpg'
    thumbnail_file_path = os.path.join('./videos', thumbnail_file_name)

    try:
        info = await downloader.download(str(url), video_file_path, thumbnail_file_path)
    except VideoTooLongError:
        await message.answer('Video is too long (max 120 seconds).')
        return

    await message.answer_video(
        FSInputFile(
            video_file_path,
            filename=video_file_name,
        ),
        supports_streaming=True,
        height=info['height'],
        width=info['width'],
        duration=int(info['duration']),
        thumbnail=FSInputFile(
            thumbnail_file_path,
            filename=thumbnail_file_name,
        ),
    )

    os.remove(video_file_path)
    os.remove(thumbnail_file_path)
