from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils import markdown as md
from datetime import datetime

from model import Station, TeamStatistic
from repository.station_repository import StationRepository
from repository.team_repository import TeamRepository
from repository.team_statistic_repository import TeamStatisticRepository

from database_command import member_commands

router = Router()


class StationCreationStates(StatesGroup):
    title = State()
    description = State()
    action = State()
    task_uuid = State()


# Все для добавления и удаления станции
# --------------------------------------------------------------------------------
@router.message(Command('add_station'))
async def start_add_station(message: types.Message, state: FSMContext):
    await message.answer("Введите заголовок станции для добавления:")
    await state.set_state(StationCreationStates.title)
    await state.update_data(action='add')


@router.message(Command('delete_station'))
async def start_delete_task(message: types.Message, state: FSMContext):
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

# --------------------------------------------------------------------------------


# Автоматическая разадача станций по каманде
# --------------------------------------------------------------------------------
@router.message(Command('start_active'))
async def start_auto_get_station(message: types.Message):
    await message.answer("Автоматическая разадача станций запущена")
    station_repository = StationRepository()
    team_repository = TeamRepository()

    stations = await station_repository.get_stations()
    teams = await team_repository.get_teams()

    if len(stations) < len(teams):
        await message.answer(f"Пожалуйста, убедитесь, что количество станций превышает количество команд")

    counter = 0
    for station in stations:
        await station_repository.update_station(station_id=station.uuid, team_uuid=teams[counter].uuid)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("Current Time =", current_time)

        new_statistic = TeamStatistic(start_time=current_time, station_uuid=station.uuid, team_uuid=teams[counter].uuid)

        team_statistic_repository = TeamStatisticRepository()
        await team_statistic_repository.create_team_statistic(new_statistic)

        counter += 1
        if counter >= len(teams):
            break

# --------------------------------------------------------------------------------
