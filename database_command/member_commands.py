import uuid
from typing import Any

from model import Station, Task
from repository.member_repository import MemberRepository
from repository.station_repository import StationRepository
from repository.task_repository import TaskRepository
from repository.team_statistic_repository import TeamStatisticRepository


async def get_station(user_id: str) -> Station:
    member_repo = MemberRepository()
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

    station = await get_station(user_id)
    if station is None:
        return None
    else:
        task_uuid = station.task_uuid
        task = await task_repo.get_task_by_id(task_uuid)
        return task


async def check_correct_response(user_id: str, user_key: str) -> bool:
    task = await get_task(user_id)

    if user_key == task.key:
        return True
    else:
        return False


async def get_possible_stations_by_team_uuid(team_uuid: uuid.UUID) -> Any:
    station_repo = StationRepository()
    team_statistic_repository = TeamStatisticRepository()

    stations = await station_repo.get_stations()
    stations_uuid_list = [stat.uuid for stat in stations]

    passed_stations = await team_statistic_repository.get_passed_stations_by_team_id(team_uuid)
    passed_stations_uuid_list = [stat.station_uuid for stat in passed_stations]

    possible_stations = set(stations_uuid_list) - set(passed_stations_uuid_list)
    return possible_stations


async def change_station(user_id: str, current_time: str, team_gave_up=False) -> int:
    member_repo = MemberRepository()
    station_repo = StationRepository()
    team_statistic_repository = TeamStatisticRepository()

    member = await member_repo.get_member_by_user_id(user_id)
    team_uuid = member.team_uuid
    current_station = await get_station(user_id)

    if current_station is None:
        pass
    else:
        current_statistic = await team_statistic_repository.get_statistic_by_team_id_station_id(team_uuid,
                                                                                                current_station.uuid)
        if team_gave_up:
            await team_statistic_repository.update_team_statistic(current_statistic.uuid,
                                                                  point=0,
                                                                  finish_time=current_time)
        else:
            await team_statistic_repository.update_team_statistic(current_statistic.uuid,
                                                                  point=1,
                                                                  finish_time=current_time)
        await station_repo.update_station(current_station.uuid, team_uuid=None)

    possible_stations = await get_possible_stations_by_team_uuid(team_uuid)

    update_flag = False
    for station_uuid in possible_stations:
        station = await station_repo.get_station_by_id(station_uuid)
        if station.team_uuid is None:
            await station_repo.update_station(station.uuid, team_uuid=team_uuid)
            update_flag = True
            break

    if len(possible_stations) == 0:
        return 2
    elif update_flag:
        return 0
    else:
        return 1
