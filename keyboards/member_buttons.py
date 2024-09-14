from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

from config.command import Commands


def start_member_kb() -> ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text=Commands.help)],
        [types.KeyboardButton(text=Commands.enter_team_token)]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Тыкай че смотришь"
    )

    return keyboard
