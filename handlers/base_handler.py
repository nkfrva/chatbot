from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from config.command import Commands
from config.help_messages import HelpMessages
from keyboards import organizer_buttons, member_buttons
from database_command import verification
from keyboards.member_buttons import start_member_kb, get_info
import os
from dotenv import load_dotenv


load_dotenv()
router = Router()


@router.message(Command(Commands.help))
async def help_command(message: Message):
    is_org, team = await verification.is_organizer(message.from_user.username)

    # org_team = os.environ.get("ORGANIZER_TEAM")
    org_team = os.getenv("ORGANIZER_TEAM")

    if is_org is False and team is None:
        await message.answer(HelpMessages.help_new_user,
                             reply_markup=member_buttons.start_member_kb())
    elif is_org is False and team is not None:
        await message.answer(HelpMessages.help_member,
                             reply_markup=member_buttons.get_info())
    elif is_org is True and team == org_team:
        await message.answer(HelpMessages.help_org,
                             reply_markup=organizer_buttons.main_menu_buttons())
    else:
        raise Exception('Invalid authentication')


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
