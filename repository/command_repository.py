import uuid

from sqlmodel import select

from model.command import Command
from config.init_db import get_session


class CommandRepository:

    async def get_commands(self) -> list[Command]:
        async with get_session() as session:
            result = await session.scalars(select(Command)).all()
            return [Command(uuid=command.uuid,
                            title=command.title,
                            description=command.description,
                            action=command.action,
                            role_uuid=command.role_uuid) for command in result]

    async def get_command_by_id(self, command_id: uuid.UUID) -> Command:
        async with get_session() as session:
            result = await session.get(Command, command_id)
            return result
