from uuid import uuid4
from sqlalchemy import Column, Integer, String, ForeignKey, UUID, Boolean, CheckConstraint
from .base_class import BaseClass
from sqlalchemy.orm import relationship

class TeamStatistic(BaseClass):

    __tablename__ = 'team_statistic'

    uuid: UUID = Column(UUID, default=uuid4, nullable=False, primary_key=True)
    point: int = Column(Integer, default=0)

    # один к одному
    team_uuid: UUID = Column(UUID, ForeignKey("team.uuid"), nullable=False, index=True)