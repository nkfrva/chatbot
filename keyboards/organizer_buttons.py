from aiogram.types import ReplyKeyboardMarkup
from aiogram import types

from config.command import Commands


def main_menu_buttons() -> ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text=Commands.menu_organizer)],
        [types.KeyboardButton(text=Commands.menu_team)],
        [types.KeyboardButton(text=Commands.menu_task)],
        [types.KeyboardButton(text=Commands.menu_station)],
        [types.KeyboardButton(text=Commands.menu_mail)],
        [types.KeyboardButton(text=Commands.menu_ban)],
        [types.KeyboardButton(text=Commands.menu_import)]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите необходимое действие"
    )

    return keyboard


def menu_team_buttons() -> ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text=Commands.add_team)],
        [types.KeyboardButton(text=Commands.remove_team)],
        [types.KeyboardButton(text=Commands.get_teams)],
        [types.KeyboardButton(text=Commands.menu_main)]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите необходимое действие"
    )

    return keyboard


def menu_organizer_buttons() -> ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text=Commands.get_leadboard)],
        [types.KeyboardButton(text=Commands.get_members)],
        [types.KeyboardButton(text=Commands.get_team_station)],
        [types.KeyboardButton(text=Commands.get_team_statistics)],
        [types.KeyboardButton(text=Commands.pin_team_to_station)],
        [types.KeyboardButton(text=Commands.unpin_team_to_station)],
        [types.KeyboardButton(text=Commands.start_active)],
        [types.KeyboardButton(text=Commands.menu_main)]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите необходимое действие"
    )

    return keyboard


def menu_task_buttons() -> ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text=Commands.add_task)],
        [types.KeyboardButton(text=Commands.remove_task)],
        [types.KeyboardButton(text=Commands.get_tasks)],
        [types.KeyboardButton(text=Commands.menu_main)]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите необходимое действие"
    )

    return keyboard


def menu_station_buttons() -> ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text=Commands.add_station)],
        [types.KeyboardButton(text=Commands.remove_station)],
        [types.KeyboardButton(text=Commands.get_stations)],
        [types.KeyboardButton(text=Commands.menu_main)]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите необходимое действие"
    )

    return keyboard


def menu_mailing_buttons() -> ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text=Commands.mailing)],
        [types.KeyboardButton(text=Commands.individual_mailing)],
        [types.KeyboardButton(text=Commands.team_mailing)],
        [types.KeyboardButton(text=Commands.menu_main)]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите необходимое действие"
    )

    return keyboard


def menu_import_buttons() -> ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text=Commands.import_tasks)],
        [types.KeyboardButton(text=Commands.import_teams)],
        [types.KeyboardButton(text=Commands.import_stations)],
        [types.KeyboardButton(text=Commands.menu_main)]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите необходимое действие"
    )

    return keyboard


def menu_ban_buttons() -> ReplyKeyboardMarkup:
    kb = [
        [types.KeyboardButton(text=Commands.ban_team)],
        [types.KeyboardButton(text=Commands.ban_user)],
        [types.KeyboardButton(text=Commands.menu_main)]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите необходимое действие"
    )

    return keyboard
