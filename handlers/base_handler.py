from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from config.command import Commands
from keyboards import organizer_buttons, member_buttons


router = Router()


@router.message(Command(Commands.start))
async def start_command(message: Message):
    await message.answer("Добро пожаловать! Присоединитесь к команде для начала работы:",
                         reply_markup=member_buttons.start_member_kb())


@router.message(lambda message: message.text == Commands.menu_main)
async def menu_main(message: Message):
    await message.answer("Главное меню",
                         reply_markup=organizer_buttons.main_menu_buttons())


@router.message(lambda message: message.text == Commands.menu_ban)
async def menu_ban(message: Message):
    await message.answer("Бан/разбан",
                         reply_markup=organizer_buttons.menu_ban_buttons())


@router.message(lambda message: message.text == Commands.menu_mail)
async def menu_mail(message: Message):
    await message.answer("Рассылка",
                         reply_markup=organizer_buttons.menu_mailing_buttons())


@router.message(lambda message: message.text == Commands.menu_task)
async def menu_task(message: Message):
    await message.answer("Задания",
                         reply_markup=organizer_buttons.menu_task_buttons())


@router.message(lambda message: message.text == Commands.menu_import)
async def menu_import(message: Message):
    await message.answer("Импорт",
                         reply_markup=organizer_buttons.menu_import_buttons())


@router.message(lambda message: message.text == Commands.menu_station)
async def menu_station(message: Message):
    await message.answer("Станции",
                         reply_markup=organizer_buttons.menu_station_buttons())


@router.message(lambda message: message.text == Commands.menu_team)
async def menu_team(message: Message):
    await message.answer("Команды",
                         reply_markup=organizer_buttons.menu_team_buttons())


@router.message(lambda message: message.text == Commands.menu_organizer)
async def menu_org(message: Message):
    await message.answer("Организационное меню",
                         reply_markup=organizer_buttons.menu_organizer_buttons())
