from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils import markdown as md

from model import Station
from repository.station_repository import StationRepository

from database_command import member_commands

router = Router()


class StationCreationStates(StatesGroup):
    title = State()
    description = State()
    action = State()
    task_uuid = State()


# Все для добавления и удаления заданий
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
            await station_repository.delete_station_by_id(existing_station)
            await message.answer(f"Станция удалена: {md.bold(existing_station.title)}")
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
