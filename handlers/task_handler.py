from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils import markdown as md

from model import Task, Key
from repository.task_repository import TaskRepository
from repository.key_repository import KeyRepository

router = Router()


class TaskCreationStates(StatesGroup):
    title = State()
    description = State()
    action = State()
    key = State()


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
        key_repository = KeyRepository()
        existing_task = await task_repository.get_task_id_by_title(task_title)
        if existing_task:
            task = await task_repository.get_task_by_id(existing_task)
            if task:
                await key_repository.delete_key_by_id(task.key_uuid)
                await message.answer(f"Ключ от задания удален")
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

    new_key = Key(key=task_key)
    key_repository = KeyRepository()
    created_key = await key_repository.create_key(new_key)
    await message.answer(f"Ключ создан: {md.bold(created_key.key)}")
    print("1")

    task_title = data.get('title')
    task_description = data.get('description')
    print(task_title)
    print(task_description)
    new_task = Task(title=task_title, description=task_description, key_uuid=created_key.uuid)
    task_repository = TaskRepository()
    created_task = await task_repository.create_task(new_task)
    print("2")

    await message.answer(f"Задание создано: {md.bold(created_task.title)}")
    await state.clear()

