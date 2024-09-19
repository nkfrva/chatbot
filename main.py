import asyncio
import logging
from aiogram import Bot, Dispatcher
from config.init_db import init_db
from handlers import organizer_handler, member_handler, team_handler, task_handler, station_handler, base_handler
import os
from dotenv import load_dotenv

bot = Bot(os.getenv(os.environ.get("BOT_TOKEN")))
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)
load_dotenv()


async def main():
    await init_db()

    dp.include_routers(organizer_handler.router,
                       member_handler.router,
                       team_handler.router,
                       task_handler.router,
                       station_handler.router,
                       base_handler.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
