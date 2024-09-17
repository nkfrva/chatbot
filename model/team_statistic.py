from uuid import uuid4
from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from .base_class import BaseClass
from sqlalchemy.orm import relationship


class TeamStatistic(BaseClass):

    __tablename__ = 'team_statistic'

    uuid: UUID = Column(UUID, default=uuid4, nullable=False, primary_key=True)
    point: int = Column(Integer, default=0)
    start_time: str = Column(String, default="time", nullable=False)
    finish_time: str = Column(String, default="time", nullable=False)

    station_uuid: UUID = Column(UUID, ForeignKey("station.uuid"), nullable=False, index=True)
    stations = relationship("Station", back_populates="team_statistic")

    team_uuid: UUID = Column(UUID, ForeignKey("team.uuid"), nullable=False, index=True)
    teams = relationship("Team", back_populates="team_statistic")
