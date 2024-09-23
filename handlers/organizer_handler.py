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
from keyboards import organizer_buttons
from keyboards.member_buttons import start_member_kb, get_info
from repository.station_repository import StationRepository
from repository.task_repository import TaskRepository
from datetime import datetime
from config.help_messages import HelpMessages

router = Router()


class MyStates(StatesGroup):
    message = State()
    team = State()
    username = State()
    individual_message = State()
    team_message = State()
    ban_user = State()
    ban_team = State()
    file = State()
    command = State()


@router.message(lambda message: message.text == Commands.mailing)
async def mail(message: types.Message, state: FSMContext):
    is_org, team = await verification.is_organizer(message.from_user.username)
    if is_org is False:
        kb = start_member_kb() if team is None else get_info()
        await message.answer('У вас нет прав доступа для выполнения данной команды.', reply_markup=kb)
        return

    await message.answer("Введите сообщение:")
    await state.set_state(MyStates.message)


@router.message(MyStates.message)
async def handle_mail(message: Message, state: FSMContext):
    member_repository = MemberRepository()
    users = await member_repository.get_members_id()
    m = message.text
    [await bot.send_message(user, m) for user in users]

    await state.clear()
    await message.answer(text='Главное меню', reply_markup=organizer_buttons.main_menu_buttons())


@router.message(StateFilter(None), lambda message: message.text == Commands.team_mailing)
async def cmd_team(message: Message, state: FSMContext):
    is_org, team = await verification.is_organizer(message.from_user.username)
    if is_org is False:
        kb = start_member_kb() if team is None else get_info()
        await message.answer('У вас нет прав доступа для выполнения данной команды.', reply_markup=kb)
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
    await state.update_data(team_mess=message.text)
    user_data = await state.get_data()

    m = user_data['team_mess']
    team = user_data['team']

    await state.clear()
    member_repository = MemberRepository()
    team_repository = TeamRepository()

    try:
        team_uuid = await team_repository.get_team_id_by_name(team)
        if team_uuid is None:
            await message.answer('Такой команды не существует',
                                 reply_markup=organizer_buttons.main_menu_buttons())
            return

        users = await member_repository.get_members_by_team_uuid(team_uuid)

        if not users:
            await message.answer('У данной команды нет участников',
                                 reply_markup=organizer_buttons.main_menu_buttons())
            return
        [await bot.send_message(user.user_id, m) for user in users]

        await message.answer(text='Главное меню', reply_markup=organizer_buttons.main_menu_buttons())

    except Exception as e:
        await message.answer(f'Во время выполнения запроса произошла ошибка {e}')
        await message.answer(text='Главное меню', reply_markup=organizer_buttons.main_menu_buttons())


@router.message(StateFilter(None), lambda message: message.text == Commands.individual_mailing)
async def cmd_user(message: Message, state: FSMContext):
    is_org, team = await verification.is_organizer(message.from_user.username)
    if is_org is False:
        kb = start_member_kb() if team is None else get_info()
        await message.answer(text='У вас нет прав доступа для выполнения данной команды.', reply_markup=kb)
        return

    await message.answer(
        text="Введите username:"
    )
    await state.set_state(MyStates.username)


@router.message(MyStates.username)
async def cmd_user_text(message: Message, state: FSMContext):
    await state.update_data(user=message.text)
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
    await state.clear()

    try:
        member_repository = MemberRepository()
        user = await member_repository.get_id_by_username(username)
        if user is None:
            await message.answer('Такого пользователя не существует. Проверьте корректность username',
                                 reply_markup=organizer_buttons.main_menu_buttons())
            return
        await bot.send_message(user.user_id, m)
        await message.answer(text='Главное меню', reply_markup=organizer_buttons.main_menu_buttons())

    except Exception as e:
        await message.answer(text=f'Во время выполнения запроса произошла ошибка {e}')
        await message.answer(text='Главное меню', reply_markup=organizer_buttons.main_menu_buttons())


@router.message(StateFilter(None), lambda message: message.text == Commands.ban_user)
async def ban_user(message: Message, state: FSMContext):
    is_org, team = await verification.is_organizer(message.from_user.username)
    if is_org is False:
        kb = start_member_kb() if team is None else get_info()
        await message.answer(text='У вас нет прав доступа для выполнения данной команды.', reply_markup=kb)
        return

    await message.answer(
        text="Введите username"
    )
    await state.set_state(MyStates.ban_user)


@router.message(MyStates.ban_user)
async def ban_by_username(message: Message, state: FSMContext):
    await state.update_data(ban=message.text.lower())
    user_data = await state.get_data()

    username = user_data['ban']
    await state.clear()

    try:
        member_repository = MemberRepository()
        user = await member_repository.ban_member_by_username(username, None)
        if user is None:
            await message.answer(text='Пользователя не существует', reply_markup=organizer_buttons.main_menu_buttons())
            return
        answer = 'забанили' if user is True else 'разбанили'

        await message.answer(f'Вы успешно {answer} {username}')
        await message.answer(text='Главное меню', reply_markup=organizer_buttons.main_menu_buttons())

    except Exception as e:
        await message.answer(text=f'Во время выполнения запроса произошла ошибка {e}')
        await message.answer(text='Главное меню', reply_markup=organizer_buttons.main_menu_buttons())


@router.message(StateFilter(None), lambda message: message.text == Commands.ban_team)
async def ban_team(message: Message, state: FSMContext):
    is_org, team = await verification.is_organizer(message.from_user.username)
    if is_org is False:
        kb = start_member_kb() if team is None else get_info()
        await message.answer(text='У вас нет прав доступа для выполнения данной команды.', reply_markup=kb)
        return

    await message.answer(
        text="Введите название команды"
    )
    await state.set_state(MyStates.ban_team)


@router.message(MyStates.ban_team)
async def ban_by_team(message: Message, state: FSMContext):
    await state.update_data(ban_team=message.text)
    user_data = await state.get_data()

    team_name = user_data['ban_team']

    team_repository = TeamRepository()
    member_repository = MemberRepository()
    station_repository = StationRepository()
    await state.clear()

    try:
        team = await team_repository.get_full_team_id_by_name(team_name)

        await team_repository.ban_team_by_uuid(team.uuid)
        users = await member_repository.get_members_by_team_uuid(team.uuid)
        stations = await station_repository.get_stations()

        if team is None:
            await message.answer(text='Команды не существует,', reply_markup=organizer_buttons.main_menu_buttons())
            return
        if not users:
            await message.answer(text='В команде нет участников', reply_markup=organizer_buttons.main_menu_buttons())
            return

        new_status = not team.ban
        [await member_repository.ban_member_by_username(user.username, new_status) for user in users]

        # освободит станцию
        station = find_station_by_team(stations, team.uuid)
        if station is not None:
            await station_repository.update_station(station_id=station.uuid, team_uuid=None)

        answer = 'разбанили' if new_status is False else 'забанили'

        await bot.send_message(message.from_user.id, f'Вы успешно {answer} команду {team_name}')
        await message.answer(text='Главное меню', reply_markup=organizer_buttons.main_menu_buttons())
    except Exception as e:
        await message.answer(text=f'Во время выполнения запроса произошла ошибка {e}')
        await message.answer(text='Главное меню', reply_markup=organizer_buttons.main_menu_buttons())


@router.message(lambda message: message.text == Commands.import_tasks or
                message.text == Commands.import_teams or
                message.text == Commands.import_stations)
async def import_task(message: types.Message, state: FSMContext):
    is_org, team = await verification.is_organizer(message.from_user.username)
    if is_org is False:
        kb = start_member_kb() if team is None else get_info()
        await message.answer('У вас нет прав доступа для выполнения данной команды.', reply_markup=kb)
        return
    await state.update_data(command=message.text)
    await message.answer(HelpMessages.help_import)
    await message.answer("Отправьте файл:")
    await state.set_state(MyStates.file)


@router.message(MyStates.file)
async def handle_task(message: types.Message, state: FSMContext):
    try:
        file_id = message.document.file_id
        data = await state.get_data()
        command = data['command']
        path = 'data/' + datetime.now().strftime("%Y%m%d%H%M") + message.document.file_name
        await download_file(file_id, path)
        await state.clear()
        if command == Commands.import_tasks:
            task_repository = TaskRepository()
            await task_repository.import_from_csv(path)

        elif command == Commands.import_teams:
            team_repository = TeamRepository()
            await team_repository.import_from_csv(path)

        elif command == Commands.import_stations:
            station_repository = StationRepository()
            await station_repository.import_from_csv(path)

        await message.answer('Файл успешно импортирован')
        await message.answer(text='Главное меню', reply_markup=organizer_buttons.main_menu_buttons())

    except Exception as e:
        await message.answer(f'Во время выполнения произошла ошибка {e}')
        await message.answer(text='Главное меню', reply_markup=organizer_buttons.main_menu_buttons())


async def download_file(file_id, path):
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, destination=path)


@router.message(lambda message: message.text == Commands.get_members)
async def get_members(message: types.Message):
    is_org, team = await verification.is_organizer(message.from_user.username)
    if is_org is False:
        kb = start_member_kb() if team is None else get_info()
        await message.answer(text='У вас нет прав доступа для выполнения данной команды.', reply_markup=kb)

    member_repository = MemberRepository()
    team_repository = TeamRepository()

    members = await member_repository.get_members()
    teams = await team_repository.get_teams()

    result = '\n'.join(f'{member.username}:'
                       f'{find_team_by_uid(teams, member.team_uuid).name}:'
                       f'{ban_text(member.ban)}' for member in members)
    await message.answer(result, reply_markup=organizer_buttons.main_menu_buttons())


@router.message(lambda message: message.text == Commands.get_team_station)
async def get_team_station(message: types.Message):
    is_org, team = await verification.is_organizer(message.from_user.username)
    if is_org is False:
        kb = start_member_kb() if team is None else get_info()
        await message.answer(text='У вас нет прав доступа для выполнения данной команды.', reply_markup=kb)

    team_repository = TeamRepository()
    station_repository = StationRepository()
    try:
        stations = await station_repository.get_stations()
        teams = await team_repository.get_teams()

        result = '\n'.join(f'{station.title}:'
                           f'{find_team_by_station(teams, station.team_uuid)}' for station in stations)
        await message.answer(result, reply_markup=organizer_buttons.main_menu_buttons())

    except Exception as e:
        await message.answer(f'Во время выполнения произошла ошибка {e}')
        await message.answer(text='Главное меню', reply_markup=organizer_buttons.main_menu_buttons())


def find_team_by_uid(teams, uuid):
    return next((team for team in teams if team.uuid == uuid), None)


def ban_text(is_ban):
    return 'забанен' if is_ban is True else 'активен'


def find_team_by_station(teams, uuid):
    return next((team.name for team in teams if team.uuid == uuid), 'станция свободна')


def find_station_by_team(stations, uuid):
    return next((station for station in stations if station.team_uuid == uuid), None)
