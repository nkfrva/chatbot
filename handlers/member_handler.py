from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

from database_command.base_commands import BaseCommands

from config.command import Commands
from config.messages import Messages
from shared.role import Role

router = Router()


@router.message(F.text.lower() == Commands.help)
async def member_help(message: Message):
    role = BaseCommands.get_role(message.from_user.username)
    if role == Role.Member or role == Role.Organizer or role == Role.Administrator:
        await message.answer(
            Messages.help_message_member,
        )
    else:
        await message.answer(
            Messages.error_message,
        )


@router.message(F.text.lower() == Commands.enter_team_token)
async def enter_team_token(message: Message):
    role = BaseCommands.get_role(message.from_user.username)
    if role != Role.Member and role != Role.Organizer and role != Role.Administrator:
        await message.answer(
            Messages.error_message,
        )

    team_token = 5
    await message.answer(
        f'Ваш токен {team_token}'
    )


