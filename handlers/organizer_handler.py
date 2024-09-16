from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from repository.member_repository import MemberRepository
from repository.team_repository import TeamRepository
from model import Member
from aiogram.utils import markdown as md
from config.command import Commands
from aiogram import types, Bot


from database_command.base_commands import BaseCommands


