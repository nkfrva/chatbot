from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from repository.member_repository import MemberRepository
from model import Member
from aiogram.utils import markdown as md

from repository.team_repository import TeamRepository
from repository.leadboard_repository import LeadboardRepository
from database_command import verification
from config.command import Commands


router = Router()


class MemberCreationStates(StatesGroup):
    team_token = State()


@router.message(Command(Commands.enter_team_token))
async def enter_team_token(message: Message, state: FSMContext):
    await message.answer("Введите уникальный идентификатор команды для присоединения:")
    await state.set_state(MemberCreationStates.team_token)


@router.message(MemberCreationStates.team_token)
async def handle_team_token(message: Message, state: FSMContext):
    user_id = message.from_user.id
    team_token = message.text

    member_repository = MemberRepository()
    team_repository = TeamRepository()

    existing_team = await team_repository.get_team_id_by_token(team_token)
    if existing_team:
        new_member = Member(team_uuid=existing_team, user_id=str(user_id), username=message.from_user.username)
        team = await team_repository.get_team_by_id(existing_team)
        await member_repository.create_member(new_member)
        await message.answer(f"вы успешно присоединились к команде: {md.bold(team.name)}")
    else:
        await message.answer("Команда не найдена.")

    await state.clear()


@router.message(Command(Commands.get_leadboard))
async def get_leadboard(message: Message, state: FSMContext):

    if await verification.is_member(message.from_user.username) is False:
        await message.answer('Вы не являетесь участником. Присоединитесь к команде.')
        return

    leadboard_repository = LeadboardRepository()
    team_repository = TeamRepository()

    await message.answer("leadboard: \n")

    leadboard_entries = await leadboard_repository.get_entries_from_leadboard()

    leadboard_string = ""
    for entry in leadboard_entries:
        team = await team_repository.get_team_by_id(entry.team_uuid)
        team_name = team.name
        leadboard_string += (f"Команда: {team_name}\n"
                             f"Пройдено станций: {entry.points}\n"
                             f"Общее время прохождения станций: {entry.passage_time}\n\n")

    await message.answer(leadboard_string)
