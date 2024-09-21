from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils import markdown as md
from datetime import datetime

from model import Task, TeamStatistic
from repository.task_repository import TaskRepository
from repository.team_statistic_repository import TeamStatisticRepository
from repository.member_repository import MemberRepository
from repository.leadboard_repository import LeadboardRepository
from config.command import Commands
from database_command import member_commands
from database_command import verification
from keyboards.member_buttons import start_member_kb, get_info
from keyboards import organizer_buttons
from handlers.station_handler import new_station

router = Router()


class TaskCreationStates(StatesGroup):
    title = State()
    description = State()
    action = State()
    key = State()
    user_key = State()


# region CRUD


# @router.message(Command(Commands.add_task))
@router.message(lambda message: message.text == Commands.add_task)
async def start_add_task(message: types.Message, state: FSMContext):
    is_member, team = await verification.is_organizer(message.from_user.username)
    if is_member is False:
        kb = start_member_kb() if team is None else get_info()
        await message.answer('У вас нет прав доступа для выполнения данной команды.', reply_markup=kb)
        return

    await message.answer("Введите заголовок задания для добавления:")
    await state.set_state(TaskCreationStates.title)
    await state.update_data(action='add')


# @router.message(Command(Commands.remove_task))
@router.message(lambda message: message.text == Commands.remove_task)
async def start_delete_task(message: types.Message, state: FSMContext):
    is_member, team = await verification.is_organizer(message.from_user.username)
    if is_member is False:
        kb = start_member_kb() if team is None else get_info()
        await message.answer('У вас нет прав доступа для выполнения данной команды.', reply_markup=kb)
        return

    await message.answer("Введите заголовок задания для удаления:")
    await state.set_state(TaskCreationStates.title)
    await state.update_data(action='delete')


@router.message(TaskCreationStates.title)
async def handle_task_title(message: types.Message, state: FSMContext):
    data = await state.get_data()
    action = data.get('action')
    task_title = message.text
    await state.clear()

    try:
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
                await message.answer(f"Задание удалено: {md.bold(existing_task.title)}",
                                     reply_markup=organizer_buttons.main_menu_buttons())
                await task_repository.delete_task_by_id(existing_task)
            else:
                await message.answer("Задание не найдено.",
                                     reply_markup=organizer_buttons.main_menu_buttons())
    except Exception as e:
        await message.answer(text='Во время выполнения запроса произошла ошибка')
        await message.answer(text='Главное меню', reply_markup=organizer_buttons.main_menu_buttons())


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

    await message.answer(f"Задание создано: {md.bold(created_task.title)}",
                         reply_markup=organizer_buttons.main_menu_buttons())
    await state.clear()


# endregion


# Когда выдана станция мы можем посмотреть
# 1. /get_station - посмотреть текущую станцию
# 2. /get_task - посмотреть текущее задание
# 3. /push_key - отправить ответ на проверку
# 4. /search_free_station - прикрепиться к свободной не пройденной станции
# --------------------------------------------------------------------------------
# @router.message(Command(Commands.get_station))
@router.message(lambda message: message.text == Commands.get_station)
async def get_station(message: types.Message):
    result_verification, mess = await verification.is_member(message.from_user.username)
    if result_verification is False:
        await message.answer(mess, reply_markup=start_member_kb())
        return

    user_id = message.from_user.id
    station = await member_commands.get_station(str(user_id))
    if station:
        await message.answer(f"Ваша текущая станция: {md.bold(station.title)} \n {md.bold(station.description)}",
                             reply_markup=get_info())
    else:
        await message.answer("Вы не прикреплены к станции", reply_markup=get_info())


# @router.message(Command(Commands.get_task))
@router.message(lambda message: message.text == Commands.get_task)
async def get_task(message: types.Message):
    result_verification, mess = await verification.is_member(message.from_user.username)
    if result_verification is False:
        await message.answer(mess, reply_markup=start_member_kb())
        return

    user_id = message.from_user.id
    task = await member_commands.get_task(str(user_id))
    if task:
        await message.answer(f"Задание: {md.bold(task.title)} \n {md.bold(task.description)}",
                             reply_markup=get_info())
    else:
        await message.answer("На данный момент нет активных заданий", reply_markup=get_info())


# @router.message(Command(Commands.push_key))
@router.message(lambda message: message.text == Commands.push_key)
async def push_key(message: types.Message, state: FSMContext):
    result_verification, mess = await verification.is_member(message.from_user.username)
    if result_verification is False:
        await message.answer(mess, reply_markup=start_member_kb())
        return

    await message.answer("Введите ответ на задание:")
    await state.set_state(TaskCreationStates.user_key)


@router.message(TaskCreationStates.user_key)
async def handle_user_key(message: types.Message, state: FSMContext):
    leadboard_repository = LeadboardRepository()
    member_repo = MemberRepository()
    team_statistic_repository = TeamStatisticRepository()

    task_user_key = message.text
    data = await state.get_data()
    user_id = message.from_user.id
    member = await member_repo.get_member_by_user_id(str(user_id))
    team_uuid = member.team_uuid
    current_station = await member_commands.get_station(str(user_id))

    task = await member_commands.get_task(str(user_id))
    if task is None:
        await message.answer(f"На данный момент вы не прикреплены к станции, поэтому ответ не может быть проверен",
                             reply_markup=get_info())
    else:
        bool_correctness = await member_commands.check_correct_response(str(user_id), task_user_key)

        if bool_correctness:
            await message.answer(f"Ответ верный! Далее вы переходите на следующую станцию", reply_markup=get_info())
            await new_station(message)

            leadboard_id = await leadboard_repository.get_leadboard_id_by_team_id(team_uuid)
            leadboard = await leadboard_repository.get_leadboard_entry_by_id(leadboard_id)

            team_statistic = await team_statistic_repository.get_statistic_by_team_id_station_id(team_uuid,
                                                                                                 current_station.uuid)

            points = leadboard.points + team_statistic.point

            current_time = datetime.strptime(leadboard.passage_time, "%H:%M:%S")
            start_time = datetime.strptime(team_statistic.start_time, "%H:%M:%S")
            finish_time = datetime.strptime(team_statistic.finish_time, "%H:%M:%S")
            new_passage_time = finish_time - start_time
            new_passage_time = current_time + new_passage_time
            new_passage_time = new_passage_time.strftime("%H:%M:%S")

            await state.clear()
            await leadboard_repository.update_leadboard_entry(leadboard_id=leadboard_id,
                                                              points=points,
                                                              passage_time=new_passage_time)
        else:
            await state.clear()
            await message.answer("Ответ не верный", reply_markup=get_info())


@router.message(lambda message: message.text == Commands.get_tasks)
async def get_tasks(message: types.Message, state: FSMContext):
    is_member, team = await verification.is_organizer(message.from_user.username)
    if is_member is False:
        kb = start_member_kb() if team is None else get_info()
        await message.answer('У вас нет прав доступа для выполнения данной команды.', reply_markup=kb)
        return

    task_repository = TaskRepository()
    try:
        tasks = await task_repository.get_tasks()
        if tasks is None:
            await message.answer('Заданий нет', reply_markup=organizer_buttons.main_menu_buttons())
            return

        result = '\n'.join(f'Задание: {task.title}, описание: {task.description}, ключ: {task.uuid}' for task in tasks)
        await message.answer(result, reply_markup=organizer_buttons.main_menu_buttons())
    except Exception as e:
        await message.answer(text='Во время выполнения запроса произошла ошибка')
        await message.answer(text='Главное меню', reply_markup=organizer_buttons.main_menu_buttons())