from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils import markdown as md

from keyboards import organizer_buttons
from keyboards.member_buttons import start_member_kb, get_info
from model import Team
from repository.team_repository import TeamRepository
from config.command import Commands
from database_command import verification

router = Router()


class TeamCreationStates(StatesGroup):
    name = State()
    action = State()


# @router.message(Command(Commands.add_team))
@router.message(lambda message: message.text == Commands.add_team)
async def start_add_team(message: types.Message, state: FSMContext):
    is_member, team = await verification.is_organizer(message.from_user.username)
    if is_member is False:
        kb = start_member_kb() if team is None else get_info()
        await message.answer('У вас нет прав доступа для выполнения данной команды.', reply_markup=kb)
        return

    await message.answer("Введите имя команды для добавления:")
    await state.set_state(TeamCreationStates.name)
    await state.update_data(action='add')


# @router.message(Command(Commands.remove_team))
@router.message(lambda message: message.text == Commands.remove_team)
async def start_delete_team(message: types.Message, state: FSMContext):
    is_member, team = await verification.is_organizer(message.from_user.username)
    if is_member is False:
        kb = start_member_kb() if team is None else get_info()
        await message.answer('У вас нет прав доступа для выполнения данной команды.', reply_markup=kb)
        return

    await message.answer("Введите имя команды для удаления:")
    await state.set_state(TeamCreationStates.name)
    await state.update_data(action='delete')


@router.message(TeamCreationStates.name)
async def handle_team_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    action = data.get('action')
    team_name = message.text

    team_repository = TeamRepository()

    await state.clear()

    if action == 'add':
        new_team = Team(name=team_name)
        created_team = await team_repository.create_team(new_team)
        await message.answer(f"Команда создана: {md.bold(created_team.name)}",
                             reply_markup=organizer_buttons.main_menu_buttons())

    elif action == 'delete':
        existing_team = await team_repository.get_team_id_by_name(team_name)
        if existing_team:
            await message.answer(f"Команда удалена: {md.bold(team_name)}",
                                 reply_markup=organizer_buttons.main_menu_buttons())
            await team_repository.delete_team_by_id(existing_team)
        else:
            await message.answer("Команда не найдена.",
                                 reply_markup=organizer_buttons.main_menu_buttons())


@router.message(lambda message: message.text == Commands.get_teams)
async def get_teams(message: types.Message, state: FSMContext):
    is_member, team = await verification.is_organizer(message.from_user.username)
    if is_member is False:
        kb = start_member_kb() if team is None else get_info()
        await message.answer('У вас нет прав доступа для выполнения данной команды.', reply_markup=kb)
        return

    team_repository = TeamRepository()
    teams = await team_repository.get_teams()

    result = '\n'.join(f'Команда: {team.name}, ключ: {team.key}' for team in teams)

    await state.clear()
    await message.answer(result, reply_markup=organizer_buttons.main_menu_buttons())
