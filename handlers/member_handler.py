from aiogram import Router, F
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
from keyboards.member_buttons import get_info, standby_kb, start_member_kb
from keyboards import organizer_buttons
from database_command import member_commands


router = Router()


class MemberCreationStates(StatesGroup):
    team_token = State()


@router.message(lambda message: message.text == Commands.enter_team_token)
async def enter_team_token(message: Message, state: FSMContext):
    await message.answer(text="Введите уникальный идентификатор команды для присоединения:")
    await state.set_state(MemberCreationStates.team_token)


@router.message(MemberCreationStates.team_token)
async def handle_team_token(message: Message, state: FSMContext):
    team_token = message.text
    username = message.from_user.username
    user_id = message.from_user.id

    member_repository = MemberRepository()
    team_repository = TeamRepository()
    await state.clear()

    try:
        existing_team = await team_repository.get_team_id_by_token(team_token)
        if existing_team:
            new_member = Member(team_uuid=existing_team, user_id=str(user_id), username=username)
            team = await team_repository.get_team_by_id(existing_team)
            await member_repository.create_member(new_member)
            is_org, _ = await verification.is_organizer(message.from_user.username)
            kb = organizer_buttons.main_menu_buttons() if is_org is True else get_info()
            await message.answer(text=f"Вы успешно присоединились к команде: {md.bold(team.name)}",
                                 reply_markup=kb)
        else:
            await message.answer(text="Команда не найдена.", reply_markup=start_member_kb())
    except Exception as e:
        await message.answer(text="Введите корректный идентификатор.", reply_markup=start_member_kb())


@router.message(lambda message: message.text == Commands.get_leadboard)
async def get_leadboard(message: Message):
    is_org, _ = await verification.is_organizer(message.from_user.username)
    kb = organizer_buttons.main_menu_buttons() if is_org is True else get_info()
    kb2 = organizer_buttons.main_menu_buttons() if is_org is True else standby_kb()

    is_member, mess = await verification.is_member(message.from_user.username)
    if is_member is False:
        await message.answer(mess, reply_markup=start_member_kb())
        return

    leadboard_repository = LeadboardRepository()
    team_repository = TeamRepository()

    user_id = message.from_user.id
    current_station = await member_commands.get_station(str(user_id))

    await message.answer("leadboard: \n")

    leadboard_entries = await leadboard_repository.get_entries_from_leadboard()
    if not leadboard_entries:
        await message.answer(text="На данный момент нет ни одной записи.",
                             reply_markup=kb)
        return

    leadboard_string = ""
    for entry in leadboard_entries:
        team = await team_repository.get_team_by_id(entry.team_uuid)
        team_name = team.name
        leadboard_string += (f"Команда: {team_name}\n"
                             f"Пройдено станций: {entry.points}\n"
                             f"Общее время прохождения станций: {entry.passage_time}\n\n")

    if current_station is None:
        await message.answer(text=leadboard_string, reply_markup=kb2)
    else:
        await message.answer(text=leadboard_string, reply_markup=kb)
