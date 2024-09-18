from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

from config.command import Commands


def organizer_start() -> ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text=Commands.start_active)],
        [types.KeyboardButton(text=Commands.mailing)],
        [types.KeyboardButton(text=Commands.individual_mailing)],
        [types.KeyboardButton(text=Commands.team_mailing)],
        [types.KeyboardButton(text=Commands.import_tasks)],
        [types.KeyboardButton(text=Commands.import_teams)],
        [types.KeyboardButton(text=Commands.import_stations)],
        [types.KeyboardButton(text=Commands.add_organizer)],
        [types.KeyboardButton(text=Commands.remove_organizer)],
        [types.KeyboardButton(text=Commands.add_team)],
        [types.KeyboardButton(text=Commands.remove_team)],
        [types.KeyboardButton(text=Commands.add_task)],
        [types.KeyboardButton(text=Commands.remove_task)],
        [types.KeyboardButton(text=Commands.add_station)],
        [types.KeyboardButton(text=Commands.remove_station)],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите необходимое действие"
    )

    return keyboard


def get_info_organizer() -> ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text=Commands.ban_team)],
        [types.KeyboardButton(text=Commands.unban_team)],
        [types.KeyboardButton(text=Commands.ban_user)],
        [types.KeyboardButton(text=Commands.unban_user)],
        [types.KeyboardButton(text=Commands.get_leadboard)],
        [types.KeyboardButton(text=Commands.add_organizer)],
        [types.KeyboardButton(text=Commands.remove_organizer)],
        [types.KeyboardButton(text=Commands.mailing)],
        [types.KeyboardButton(text=Commands.individual_mailing)],
        [types.KeyboardButton(text=Commands.team_mailing)],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите необходимое действие"
    )

    return keyboard