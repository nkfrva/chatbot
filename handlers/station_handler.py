from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils import markdown as md
from datetime import datetime

from model import Station, TeamStatistic, LeadBoard
from repository.station_repository import StationRepository
from repository.team_repository import TeamRepository
from repository.team_statistic_repository import TeamStatisticRepository
from repository.leadboard_repository import LeadboardRepository
from config.command import Commands
from database_command import verification


router = Router()


class StationCreationStates(StatesGroup):
    title = State()
    description = State()
    action = State()
    task_uuid = State()


# region CRUD station

@router.message(Command(Commands.add_station))
async def start_add_station(message: types.Message, state: FSMContext):
    if await verification.is_organizer(message.from_user.username) is False:
        await message.answer('У вас нет прав доступа для выполнения данной команды.')
        return

    await message.answer("Введите заголовок станции для добавления:")
    await state.set_state(StationCreationStates.title)
    await state.update_data(action='add')


@router.message(Command(Commands.remove_station))
async def start_delete_task(message: types.Message, state: FSMContext):
    if await verification.is_organizer(message.from_user.username) is False:
        await message.answer('У вас нет прав доступа для выполнения данной команды.')
        return

    await message.answer("Введите заголовок станции для удаления:")
    await state.set_state(StationCreationStates.title)
    await state.update_data(action='delete')


@router.message(StationCreationStates.title)
async def handle_station_title(message: types.Message, state: FSMContext):
    data = await state.get_data()
    action = data.get('action')
    station_title = message.text

    if action == 'add':
        await message.answer("Введите описание станции:")
        await state.set_state(StationCreationStates.description)
        await state.update_data(title=station_title)
        return

    elif action == 'delete':
        station_repository = StationRepository()
        existing_station = await station_repository.get_station_id_by_title(station_title)
        if existing_station:
            await message.answer(f"Станция удалена: {md.bold(existing_station.title)}")
            await station_repository.delete_station_by_id(existing_station)
        else:
            await message.answer("Станция не найдена")

        await state.clear()


@router.message(StationCreationStates.description)
async def handle_station_description(message: types.Message, state: FSMContext):
    station_description = message.text
    data = await state.get_data()
    station_title = data.get('title')

    await message.answer("Введите uuid задания:")
    await state.set_state(StationCreationStates.task_uuid)
    await state.update_data(description=station_description)


@router.message(StationCreationStates.task_uuid)
async def handle_task_uuid(message: types.Message, state: FSMContext):
    data = await state.get_data()
    station_uuid = message.text

    station_title = data.get('title')
    station_description = data.get('description')
    new_station = Station(title=station_title, description=station_description, task_uuid=station_uuid)

    station_repository = StationRepository()
    created_station = await station_repository.create_station(new_station)

    await message.answer(f"Станция создана: {md.bold(created_station.title)}")
    await state.clear()

# endregion

# region Automatic station assignment on command


@router.message(Command(Commands.start_active))
async def start_auto_get_station(message: types.Message):
    if await verification.is_organizer(message.from_user.username) is False:
        await message.answer('У вас нет прав доступа для выполнения данной команды.')
        return

    station_repository = StationRepository()
    team_repository = TeamRepository()
    team_statistic_repository = TeamStatisticRepository()
    leadboard_repository = LeadboardRepository()

    await message.answer("Автоматическая разадача станций запущена")

    stations = await station_repository.get_stations()
    teams = await team_repository.get_teams()

    if len(stations) < len(teams):
        await message.answer(f"Пожалуйста, убедитесь, что количество станций превышает количество команд")

    counter = 0
    for station in stations:
        await station_repository.update_station(station_id=station.uuid, team_uuid=teams[counter].uuid)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        new_statistic = TeamStatistic(start_time=current_time, station_uuid=station.uuid, team_uuid=teams[counter].uuid)
        await team_statistic_repository.create_team_statistic(new_statistic)

        new_leadboard = LeadBoard(team_uuid=teams[counter].uuid)
        await leadboard_repository.create_leadboard_entry(new_leadboard)

        counter += 1
        if counter >= len(teams):
            break

    await message.answer(f"Все команды успешно присоединены к станциям")

# endregion
