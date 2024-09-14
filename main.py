import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from config.init_db import init_db

logging.basicConfig(level=logging.INFO)
bot = Bot(token="7482379369:AAH-3lqEjFSN8CyUsjfr8W5Xdu5mcFc8bO4")
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


# @dp.on_event("startup")
# def on_startup():
#     init_db()

async def main():
    await init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
