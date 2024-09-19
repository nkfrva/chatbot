import os
# from dotenv import load_dotenv

from repository.member_repository import MemberRepository
from repository.team_repository import TeamRepository

# load_dotenv()
member_repository = MemberRepository()
team_repository = TeamRepository


async def is_organizer(username: str) -> bool:
    user = await member_repository.get_id_by_username(username)
    team = await team_repository.get_team_by_id(user.team_uuid)

    org_team = os.environ.get("ORGANIZER_TEAM")

    return team.name == org_team


async def is_member(username: str):
    try:
        user = await member_repository.get_id_by_username(username)
        team = await team_repository.get_team_by_id(user.team_uuid)

        message = 'Вы забанены' if user.ban is True \
            else 'Вы не являетесь участником. Присоединитесь к команде.'

        return team.name is not None and user.ban is False, message
    except RuntimeError:
        return False
