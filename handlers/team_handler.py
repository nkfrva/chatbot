from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils import markdown as md

from model import Team
from repository.team_repository import TeamRepository

router = Router()


class TeamCreationStates(StatesGroup):
    name = State()
    action = State()


@router.message(Command('add_team'))
async def start_add_team(message: types.Message, state: FSMContext):
    await message.answer("Введите имя команды для добавления:")
    await state.set_state(TeamCreationStates.name)
    await state.update_data(action='add')


@router.message(Command('delete_team'))
async def start_delete_team(message: types.Message, state: FSMContext):
    await message.answer("Введите имя команды для удаления:")
    await state.set_state(TeamCreationStates.name)
    await state.update_data(action='delete')


@router.message(TeamCreationStates.name)
async def handle_team_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    action = data.get('action')
    team_name = message.text

    team_repository = TeamRepository()

    if action == 'add':
        new_team = Team(name=team_name)
        created_team = await team_repository.create_team(new_team)
        await message.answer(f"Команда создана: {md.bold(created_team.name)}")

    elif action == 'delete':
        existing_team = await team_repository.get_team_id_by_name(team_name)
        if existing_team:
            await team_repository.delete_team_by_id(existing_team)  # Assuming you have this method
            await message.answer(f"Команда удалена: {md.bold(team_name)}")
        else:
            await message.answer("Команда не найдена.")

    await state.clear()
