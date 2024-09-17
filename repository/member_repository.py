import uuid

from sqlmodel import select
from sqlmodel import Session

from model.member import Member
from config.init_db import get_session


class MemberRepository:
    async def get_members(self) -> list[Member]:
        async with get_session() as session:
            result = await session.execute(select(Member))
            return result.scalars().all()

    async def get_members_id(self) -> list[int]:
        async with get_session() as session:
            result = await session.execute(select(Member.user_id))
            return result.scalars().all()

    async def get_members_id_by_team_uuid(self, team_uuid: str) -> list[int]:
        async with get_session() as session:
            result = await session.execute(select(Member.user_id).where(Member.team_uuid == team_uuid))
            return result.scalars().all()

    async def get_member_by_id(self, member_id: uuid.UUID) -> Member:
        async with get_session() as session:
            result = await session.get(Member, member_id)
            return result

    async def get_id_by_username(self, username: str) -> id:
        async with get_session() as session:
            result = await session.execute(select(Member.user_id).where(Member.username == username))
            return result.scalars().first()


    async def get_member_by_user_id(self, user_id: str) -> Member:
        async with get_session() as session:
            result = await session.execute(select(Member).where(Member.user_id == user_id))
            member = result.scalars().first()
            return member

    async def create_member(self, new_member: Member) -> Member:
        async with get_session() as session:
            session.add(new_member)
            await session.commit()
            await session.refresh(new_member)
            return new_member

    async def delete_member_by_id(self, member_id: uuid.UUID) -> bool:
        async with get_session() as session:
            result = await session.get(Member, member_id)

            if result is None:
                return False

            await session.delete(result)
            await session.commit()
            return True
