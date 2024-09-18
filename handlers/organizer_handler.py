from aiogram import Router, F
from aiogram.types import Message
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from main import bot
from repository.member_repository import MemberRepository
from repository.team_repository import TeamRepository
from aiogram.filters import Command, StateFilter
from config.command import Commands
from database_command import verification
from keyboards.organizer_buttons import organizer_start, get_info_organizer


router = Router()


class MyStates(StatesGroup):
    message = State()
    team = State()
    username = State()
    individual_message = State()
    team_message = State()
    ban_user = State()
    ban_team = State()


# @router.message(Command(Commands.mailing))
@router.message(lambda message: message.text == Commands.mailing)
async def mail(message: types.Message, state: FSMContext):
    if await verification.is_organizer(message.from_user.username) is False:
        await message.answer('У вас нет прав доступа для выполнения данной команды.')
        return

    await message.answer("Введите сообщение:")
    await state.set_state(MyStates.message)


@router.message(MyStates.message)
async def handle_mail(message: Message, state: FSMContext):
    member_repository = MemberRepository()
    users = await member_repository.get_members_id()
    m = message.text
    [await bot.send_message(user, m) for user in users]
    await message.answer(text="", reply_markup=get_info_organizer())
    await state.clear()


# @router.message(StateFilter(None), Command(Commands.team_mailing))
@router.message(StateFilter(None), lambda message: message.text == Commands.team_mailing)
async def cmd_team(message: Message, state: FSMContext):
    if await verification.is_organizer(message.from_user.username) is False:
        await message.answer('У вас нет прав доступа для выполнения данной команды.')
        return

    await message.answer(
        text="Введите команду:"
    )
    await state.set_state(MyStates.team)


@router.message(MyStates.team)
async def cmd_team_text(message: Message, state: FSMContext):
    await state.update_data(team=message.text)
    await message.answer(
        text="Введите сообщение:",
    )
    await state.set_state(MyStates.team_message)


@router.message(MyStates.team_message)
async def cmd_team_send(message: Message, state: FSMContext):
    await state.update_data(team_mess=message.text.lower())
    user_data = await state.get_data()

    m = user_data['team_mess']
    team = user_data['team']

    member_repository = MemberRepository()
    team_repository = TeamRepository()

    team_uuid = await team_repository.get_team_id_by_name(team)
    users = await member_repository.get_members_by_team_uuid(team_uuid)
    [await bot.send_message(user.user_id, m) for user in users]

    await message.answer(text="", reply_markup=get_info_organizer())
    await state.clear()


# @router.message(StateFilter(None), Command(Commands.individual_mailing))
@router.message(StateFilter(None), lambda message: message.text == Commands.individual_mailing)
async def cmd_user(message: Message, state: FSMContext):
    if await verification.is_organizer(message.from_user.username) is False:
        await message.answer('У вас нет прав доступа для выполнения данной команды.')
        return

    await message.answer(
        text="Введите username:"
    )
    await state.set_state(MyStates.username)


@router.message(MyStates.username)
async def cmd_user_text(message: Message, state: FSMContext):
    await state.update_data(user=message.text.lower())
    await message.answer(
        text="Введите сообщение:",
    )
    await state.set_state(MyStates.individual_message)


@router.message(MyStates.individual_message)
async def cmd_user_send(message: Message, state: FSMContext):
    await state.update_data(user_mess=message.text.lower())
    user_data = await state.get_data()

    m = user_data['user_mess']
    username = user_data['user']

    member_repository = MemberRepository()
    user = await member_repository.get_id_by_username(username)

    await bot.send_message(user.user_id, m)
    await message.answer(text="", reply_markup=get_info_organizer())
    await state.clear()


@router.message(StateFilter(None), Command(Commands.ban_user))
async def ban_user(message: Message, state: FSMContext):
    if await verification.is_organizer(message.from_user.username) is False:
        await message.answer('У вас нет прав доступа для выполнения данной команды.')
        return

    await message.answer(
        text="Введите username"
    )
    await state.set_state(MyStates.ban_user)


@router.message(MyStates.ban_user)
async def ban(message: Message, state: FSMContext):
    await state.update_data(ban=message.text.lower())
    user_data = await state.get_data()

    username = user_data['ban']

    member_repository = MemberRepository()
    user = await member_repository.ban_member_by_username(username)
    answer = 'забанили' if user is True else 'разбанили'

    await bot.send_message(message.from_user.id, f'Вы успешно {answer} {username}')
    await state.clear()


@router.message(StateFilter(None), Command(Commands.ban_team))
async def ban_user(message: Message, state: FSMContext):
    if await verification.is_organizer(message.from_user.username) is False:
        await message.answer('У вас нет прав доступа для выполнения данной команды.')
        return

    await message.answer(
        text="Введите название команды"
    )
    await state.set_state(MyStates.ban_team)


@router.message(MyStates.ban_team)
async def ban_team(message: Message, state: FSMContext):
    await state.update_data(ban_team=message.text)
    user_data = await state.get_data()

    team_name = user_data['ban_team']

    team_repository = TeamRepository()
    member_repository = MemberRepository()

    team = await team_repository.get_team_id_by_name(team_name)
    users = await member_repository.get_members_by_team_uuid(team)

    [await member_repository.ban_member_by_username(user.username) for user in users]
    answer = 'забанили' if users[0].ban is True else 'разбанили'

    await bot.send_message(message.from_user.id, f'Вы успешно {answer} команду {team_name}')
    await state.clear()
