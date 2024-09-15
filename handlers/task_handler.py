from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils import markdown as md

from model import Task
from repository.task_repository import TaskRepository

from database_command import member_commands

router = Router()


class TaskCreationStates(StatesGroup):
    title = State()
    description = State()
    action = State()
    key = State()
    user_key = State()


# Все для добавления и удаления заданий
# --------------------------------------------------------------------------------
@router.message(Command('add_task'))
async def start_add_task(message: types.Message, state: FSMContext):
    await message.answer("Введите заголовок задания для добавления:")
    await state.set_state(TaskCreationStates.title)
    await state.update_data(action='add')


@router.message(Command('delete_task'))
async def start_delete_task(message: types.Message, state: FSMContext):
    await message.answer("Введите заголовок задания для удаления:")
    await state.set_state(TaskCreationStates.title)
    await state.update_data(action='delete')


@router.message(TaskCreationStates.title)
async def handle_task_title(message: types.Message, state: FSMContext):
    data = await state.get_data()
    action = data.get('action')
    task_title = message.text

    if action == 'add':
        await message.answer("Введите описание задания:")
        await state.set_state(TaskCreationStates.description)
        await state.update_data(title=task_title)
        return

    elif action == 'delete':
        task_repository = TaskRepository()
        # key_repository = KeyRepository()
        existing_task = await task_repository.get_task_id_by_title(task_title)
        if existing_task:
            await task_repository.delete_task_by_id(existing_task)
            await message.answer(f"Задание удалено: {md.bold(existing_task.title)}")
        else:
            await message.answer("Задание не найдено.")

        await state.clear()


@router.message(TaskCreationStates.description)
async def handle_task_description(message: types.Message, state: FSMContext):
    task_description = message.text
    data = await state.get_data()
    task_title = data.get('title')

    await message.answer("Введите ответ на задание:")
    await state.set_state(TaskCreationStates.key)
    await state.update_data(description=task_description)


@router.message(TaskCreationStates.key)
async def handle_task_answer(message: types.Message, state: FSMContext):
    data = await state.get_data()
    task_key = message.text

    task_title = data.get('title')
    task_description = data.get('description')
    new_task = Task(title=task_title, description=task_description, key=task_key)

    task_repository = TaskRepository()
    created_task = await task_repository.create_task(new_task)

    await message.answer(f"Задание создано: {md.bold(created_task.title)}")
    await state.clear()

# --------------------------------------------------------------------------------


# Когда выдана станция мы можем посмотреть
# 1. /get_station - посмотреть текущую станцию
# 2. /get_task - посмотреть текущее задание
# 3. /push_key - отправить ответ на проверку
# --------------------------------------------------------------------------------
@router.message(Command('get_station'))
async def get_station(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    station = await member_commands.get_station(str(user_id))
    if station:
        await message.answer(f"Ваша текущая станция: {md.bold(station.title)} \n {md.bold(station.description)}")
    else:
        await message.answer("Вы не прикреплены к станции")


@router.message(Command('get_task'))
async def get_task(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    task = await member_commands.get_task(str(user_id))
    if task:
        await message.answer(f"Ваша текущая станция: {md.bold(task.title)} \n {md.bold(task.description)}")
    else:
        await message.answer("На данный момент нет активных заданий")


@router.message(Command('push_key'))
async def push_key(message: types.Message, state: FSMContext):
    await message.answer("Введите ответ на задание:")
    await state.set_state(TaskCreationStates.user_key)


@router.message(TaskCreationStates.user_key)
async def handle_user_key(message: types.Message, state: FSMContext):
    task_user_key = message.text
    data = await state.get_data()

    user_id = message.from_user.id
    bool_correctness = await member_commands.check_correct_response(str(user_id), task_user_key)
    if bool_correctness:
        await message.answer(f"Успех! Ответ верный. Далее вы переходите на следующую станцию")
    else:
        await message.answer("Ответ не верный")

    await state.clear()