import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import routers
from settings import app_settings


dp = Dispatcher()
dp.include_routers(*routers)


async def main() -> None:
    bot = Bot(
        token=app_settings.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
    )
    logging.getLogger('httpx').setLevel(logging.WARNING)

    try:
        import uvloop
    except ImportError:
        asyncio.run(main())
    else:
        uvloop.run(main())
