from uuid import uuid4
from sqlalchemy import Column, Integer, String, ForeignKey, UUID, CheckConstraint
from sqlalchemy.orm import relationship
from .base_class import BaseClass


class Team(BaseClass):

    __tablename__ = 'team'

    uuid: UUID = Column(UUID, default=uuid4, nullable=False, primary_key=True)
    key: UUID = Column(UUID, default=uuid4, nullable=False, primary_key=False)
    name: str = Column(String, default="Loxi", nullable=False)

    members = relationship("Member", back_populates="teams")

    # один к одному
    # не надо хранить uuid статистики!!!
    team_statistic = relationship("TeamStatistic", back_populates="teams", uselist=False)

    stations = relationship("Station", back_populates="team", uselist=False)
