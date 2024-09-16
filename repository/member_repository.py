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

    async def get_member_by_id(self, member_id: uuid.UUID) -> Member:
        async with get_session() as session:
            result = await session.get(Member, member_id)
            return result

    async def get_member_by_user_id(self, user_id: str) -> Member:
        async with get_session() as session:
            result = await session.execute(select(Member).where(Member.user_id == user_id))
            station = result.scalars().first()
            return station

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

    # def get_members(self) -> list[Member]:
    #     session: Session = next(get_session())
    #     result = session.scalars(select(Member)).all()
    #     session.close()
    #     return [Member(uuid=member.uuid,
    #                    team_uuid=member.team_uuid,
    #                    role_uuid=member.role_uuid) for member in result]
    #
    # def get_member_by_id(self, member_id: uuid.UUID) -> Member:
    #     session: Session = next(get_session())
    #     result = session.get(Member, member_id)
    #     session.close()
    #     return result
    #
    # def create_member(self, member_create: Member, team_uuid: uuid, role_uuid: uuid) -> Member:
    #     session: Session = next(get_session())
    #     new_member = LeadBoard(team_uuid=team_uuid,
    #                           role_uuid=role_uuid)
    #
    #     session.add(new_member)
    #     session.commit()
    #     session.refresh(new_member)
    #     session.close()
    #     return new_member
    #
    # def delete_member_by_id(self, member_id: uuid.UUID) -> bool:
    #     session: Session = next(get_session())
    #     result = session.get(Member, member_id)
    #
    #     if result is None:
    #         return False
    #
    #     session.delete(result)
    #     session.commit()
    #     session.close()
    #     return True
