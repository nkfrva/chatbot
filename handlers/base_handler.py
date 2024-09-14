from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message

from shared.role import Role
from config.command import Commands
from config.messages import Messages
from database_command.base_commands import BaseCommands
from keyboards.member_buttons import start_member_kb

router = Router()


@router.message(Command(Commands.start))
async def cmd_start(message: Message):

    role = BaseCommands.register(message.from_user.username)

    if role == Role.Administrator:
        print('a')
    elif role == Role.Organizer:
        print('o')
    elif role == Role.Member:
        await message.answer(
            Messages.hello_message_member,
            reply_markup=start_member_kb()
        )
    else:
        await message.answer(
            Messages.error_message
        )
    # добавить возможность закрытия регистрации




