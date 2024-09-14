import asyncio
import logging
from aiogram import Bot, Dispatcher
from config.init_db import init_db
from handlers import base_handler, member_handler


logging.basicConfig(level=logging.INFO)


async def main():
    await init_db()

    bot = Bot(token="7504919443:AAHIAuAr8lhDGcAyyytaMG-zzGWl6pSrUec")
    dp = Dispatcher()

    dp.include_routers(base_handler.router, member_handler.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
