import uuid
from sqlmodel import select

from model.member import Member
from config.init_db import get_session


class MemberRepository:

    @staticmethod
    async def get_members() -> list[Member]:
        async with get_session() as session:
            result = await session.execute(select(Member))
            return result.scalars().all()

    @staticmethod
    async def get_members_id() -> list[int]:
        async with get_session() as session:
            result = await session.execute(select(Member.user_id))
            return result.scalars().all()

    @staticmethod
    async def get_member_by_id(member_id: uuid.UUID) -> Member:
        async with get_session() as session:
            result = await session.get(Member, member_id)
            return result

    @staticmethod
    async def get_member_by_user_id(user_id: str) -> Member:
        async with get_session() as session:
            result = await session.execute(select(Member).where(Member.user_id == user_id))
            member = result.scalars().first()
            return member

    @staticmethod
    async def get_members_by_team_uuid(team_uuid: str) -> list[Member]:
        async with get_session() as session:
            result = await session.execute(select(Member).where(Member.team_uuid == team_uuid))
            return result.scalars().all()

    @staticmethod
    async def get_id_by_username(username: str) -> Member:
        async with get_session() as session:
            result = await session.execute(select(Member).where(Member.username == username))
            return result.scalars().first()

    @staticmethod
    async def ban_member_by_username(username: str, value) -> bool:
        async with get_session() as session:
            result = await session.execute(select(Member).where(Member.username == username))
            member = result.scalars().first()

            new_value = not member.ban if value is None else value
            member.ban = new_value

            await session.commit()
            await session.refresh(member)
            return new_value


    # region CRUD

    @staticmethod
    async def create_member(new_member: Member) -> Member:
        async with get_session() as session:
            existing_users = await session.execute(select(Member).where(Member.user_id == new_member.user_id))
            existing_user = existing_users.scalars().first()
            if existing_user is not None:
                return existing_user

            session.add(new_member)
            await session.commit()
            await session.refresh(new_member)
            return new_member

    @staticmethod
    async def delete_member_by_id(member_id: uuid.UUID) -> bool:
        async with get_session() as session:
            result = await session.get(Member, member_id)

            if result is None:
                return False

            await session.delete(result)
            await session.commit()
            return True

    # endregion
