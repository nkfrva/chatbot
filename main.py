import asyncio
import logging
from aiogram import Bot, Dispatcher
from config.init_db import init_db
from handlers import base_handler, member_handler, team_handler, task_handler, station_handler
import uuid
from repository import role_repository
from model import role
logging.basicConfig(level=logging.INFO)


async def main():
    await init_db()

    bot = Bot(token="7482379369:AAH-3lqEjFSN8CyUsjfr8W5Xdu5mcFc8bO4")
    dp = Dispatcher()

    dp.include_routers(member_handler.router, team_handler.router, task_handler.router, station_handler.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
