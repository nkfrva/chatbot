from uuid import uuid4
from sqlalchemy import Column, String, UUID, Boolean
from sqlalchemy.orm import relationship
from .base_class import BaseClass


class Team(BaseClass):

    __tablename__ = 'team'

    uuid: UUID = Column(UUID, default=uuid4, nullable=False, primary_key=True)
    key: UUID = Column(UUID, default=uuid4, nullable=False, primary_key=False)
    name: str = Column(String, default="team", nullable=False)
    ban: bool = Column(Boolean, default='False', nullable=False)

    members = relationship("Member", back_populates="teams")
    team_statistic = relationship("TeamStatistic", back_populates="teams")
    stations = relationship("Station", back_populates="team", uselist=False)
