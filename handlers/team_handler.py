from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils import markdown as md
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove

from database_command.base_commands import BaseCommands

from config.command import Commands
from config.messages import Messages
from model import Team
from repository.team_repository import TeamRepository
from repository.team_statistic_repository import TeamStatisticRepository
from config.init_db import get_session


router = Router()


class TeamCreationStates(StatesGroup):
    name = State()


@router.message(Command('add_team'))
async def start_team_creation(message: types.Message, state: FSMContext):
    await message.answer("Введите имя команды:")
    await state.set_state(TeamCreationStates.name)


@router.message(TeamCreationStates.name)
async def get_team_name(message: types.Message, state: FSMContext):
    team_name = message.text

    # team_statistic = TeamStatisticRepository().create_team_statistic()
    # Create a new team
    new_team = Team(name=team_name)

    # Save the team to the database using TeamRepository
    created_team = await TeamRepository().create_team(new_team)

    await message.answer(f"Команда создана: {md.bold(created_team.name)}")
    await state.clear()


# @router.message(F.text.lower() == Commands.add_team)
# async def add_team(message: Message):
#     print("Дурочка")
#     await message.answer(
#         Messages.error_message,
#     )
#
#     # Запросить имя команды у пользователя
#     await message.answer("Введите имя команды:")
#
#     # Ожидать ответа от пользователя
#     team_name_message = await router.message(F.text)(message)
#
#     # Запросить описание команды у пользователя
#     await message.answer("Введите описание команды:")
#
#     # Ожидать ответа от пользователя
#     team_description_message = await router.message(F.text)(message)
#
#     # Создать новую команду с полученными атрибутами
#     new_team = Team(name=team_name_message.text, description=team_description_message.text)
#
#     # Вызвать функцию create_team
#     created_team = await TeamRepository.create_team(new_team)
#
#     # Отправить ответ пользователю
#     await message.answer(f"Команда создана: {created_team.name}")


