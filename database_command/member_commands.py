import uuid

from repository.member_repository import MemberRepository
from repository.team_repository import TeamRepository
from repository.station_repository import StationRepository
from repository.task_repository import TaskRepository
from model import Member, Team, Station, Task


async def get_station(user_id: str) -> Station:
    member_repo = MemberRepository()
    team_repo = TeamRepository()
    station_repo = StationRepository()

    member = await member_repo.get_member_by_user_id(user_id)
    team_uuid = member.team_uuid

    station = await station_repo.get_station_by_team_uuid(team_uuid)
    if station:
        return station
    else:
        return None


async def get_task(user_id: str) -> Task:
    task_repo = TaskRepository()
    station_repo = StationRepository()

    station = await get_station(user_id)
    task_uuid = station.task_uuid

    task = await task_repo.get_task_by_id(task_uuid)
    return task


async def check_correct_response(user_id, user_key):
    task = await get_task(user_id)
    if user_key == task.key:
        return True
    else:
        return False
