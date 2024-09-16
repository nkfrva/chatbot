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
from repository.member_repository import MemberRepository
from repository.team_repository import TeamRepository


router = Router()


class MyStates(StatesGroup):
    message = State()



@router.message(Command('mail'))
async def start_add_task(message: types.Message, state: FSMContext):
    await message.answer("Введите сообщение")
    await state.set_state(MyStates.message)


@router.message(MyStates.message)
async def handle_team_token(message: Message, state: FSMContext):
    member_repository = MemberRepository()
    users = await member_repository.get_members_id()
    m = message.text
    [await bot.send_message(user, m) for user in users]

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




