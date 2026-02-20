from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.types import Message


router = Router()

message = """
Hello, {user_name}!

You can use this bot to download YouTube Shorts, Reels and TikTok videos.
Usage:
/download <video_url> - Download a video from the provided URL.
"""


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        message.format(user_name=html.quote(message.from_user.first_name)),  # type: ignore
    )
