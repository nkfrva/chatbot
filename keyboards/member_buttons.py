from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

from config.command import Commands


def start_member_kb() -> ReplyKeyboardMarkup:
    kb = [
        # [types.KeyboardButton(text=Commands.help)],
        [types.KeyboardButton(text=Commands.enter_team_token)]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Нажмите на кнопку"
    )

    return keyboard


def get_info() -> ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text=Commands.get_station)],
        [types.KeyboardButton(text=Commands.get_task)],
        [types.KeyboardButton(text=Commands.push_key)],
        [types.KeyboardButton(text=Commands.get_leadboard)],
        [types.KeyboardButton(text=Commands.detach_team)]

    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите необходимое действие"
    )

    return keyboard


def standby_kb() -> ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text=Commands.search_free_station)],
        [types.KeyboardButton(text=Commands.get_leadboard)],
    ]

    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите необходимое действие"
    )

    return keyboard
