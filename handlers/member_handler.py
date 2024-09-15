from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from repository.member_repository import MemberRepository
from repository.team_repository import TeamRepository
from model import Member
from aiogram.utils import markdown as md


router = Router()


class MemberCreationStates(StatesGroup):
    team_token = State()


@router.message(Command('enter_team_token'))
async def enter_team_token(message: Message, state: FSMContext):
    await message.answer("Введите уникальный идентификатор команды для присоединения:")
    await state.set_state(MemberCreationStates.team_token)


@router.message(MemberCreationStates.team_token)
async def handle_team_token(message: Message, state: FSMContext):
    team_token = message.text

    member_repository = MemberRepository()
    team_repository = TeamRepository()

    existing_team = await team_repository.get_team_id_by_token(team_token)
    if existing_team:
        new_member = Member(team_uuid=existing_team)
        team = await team_repository.get_team_by_id(existing_team)
        await member_repository.create_member(new_member)
        await message.answer(f"вы успешно присоединились к команде: {md.bold(team.name)}")
    else:
        await message.answer("Команда не найдена.")

    await state.clear()




