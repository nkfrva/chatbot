import uuid

from sqlmodel import select
from sqlmodel import Session

from model.role import Role
from config.init_db import get_session


class RoleRepository:
    async def get_roles(self) -> list[Role]:
        async with get_session() as session:
            result = await session.exec(select(Role)).all()
            return [Role(uuid=role.uuid,
                         title=role.title) for role in result]

    async def get_role_by_id(self, role_id: uuid.UUID) -> Role:
        async with get_session() as session:
            result = await session.get(Role, role_id)
            return result

    # def get_roles(self) -> list[Role]:
    #     session: Session = next(get_session())
    #     result = session.scalars(select(Role)).all()
    #     session.close()
    #     return [Role(uuid=role.uuid,
    #                    title=role.title) for role in result]
    #
    # def get_role_by_id(self, role_id: uuid.UUID) -> Role:
    #     session: Session = next(get_session())
    #     result = session.get(Role, role_id)
    #     session.close()
    #     return result

