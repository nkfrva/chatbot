from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from repository.member_repository import MemberRepository
from model import Member
from aiogram.utils import markdown as md

from repository.team_repository import TeamRepository
from repository.leadboard_repository import LeadboardRepository
from database_command import verification
from config.command import Commands
from keyboards.member_buttons import start_member_kb


router = Router()


@router.message(Command(Commands.start))
async def start_command(message: Message):
    await message.answer("Добро пожаловать! Присоединитесь к команде для начала работы:",
                         reply_markup=start_member_kb())
