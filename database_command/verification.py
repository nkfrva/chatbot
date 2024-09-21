import os
# from dotenv import load_dotenv

from repository.member_repository import MemberRepository
from repository.team_repository import TeamRepository

# load_dotenv()
member_repository = MemberRepository()
team_repository = TeamRepository


async def is_organizer(username: str):
    try:
        user = await member_repository.get_id_by_username(username)
        team = await team_repository.get_team_by_id(user.team_uuid)

        org_team = os.environ.get("ORGANIZER_TEAM")
        # org_team = os.getenv("ORGANIZER_TEAM")

        return team.name == org_team, team.name

    except Exception as e:
        return False, None


async def is_member(username: str):
    try:
        user = await member_repository.get_id_by_username(username)
        team = await team_repository.get_team_by_id(user.team_uuid)

        message = 'Вы забанены' if user.ban is True \
            else 'Вы не являетесь участником. Присоединитесь к команде.'

        return team.name is not None and user.ban is False, message
    except Exception as e:
        return False, 'Во время выполнения запроса произошла ошибка.'
