from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import types
from shared.role import Role
from config.command import Commands
from config.messages import Messages
from keyboards.member_buttons import start_member_kb
from repository import member_repository
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from main import bot

router = Router()


class MyStates(StatesGroup):
    message = State()



@router.message(Command('mail'))
async def start_add_task(message: types.Message, state: FSMContext):
    await message.answer("Введите заголовок задания для добавления:")
    await state.set_state(MyStates.message)


@router.message(MyStates.message)
async def handle_team_token(message: Message, state: FSMContext):
    user_id = message.from_user.id
    m = message.text
    await bot.send_message(726067906, m)
    await bot.send_message(798162397, m)
    await state.clear()



# @router.message(Command(Commands.start))
# async def cmd_start(message: Message):
#
#     role = BaseCommands.register(message.from_user.username)
#
#     if role == Role.Administrator:
#         print('a')
#     elif role == Role.Organizer:
#         print('o')
#     elif role == Role.Member:
#
#         await message.answer(
#             Messages.hello_message_member,
#             reply_markup=start_member_kb()
#         )
#     else:
#         await message.answer(
#             Messages.error_message
#         )
#     # добавить возможность закрытия регистрации




