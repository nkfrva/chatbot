from uuid import uuid4
from sqlalchemy import Column, Integer, String, ForeignKey, UUID, CheckConstraint
from sqlalchemy.orm import relationship
from .base_class import BaseClass


class Team(BaseClass):

    __tablename__ = 'team'

    uuid: UUID = Column(UUID, default=uuid4, nullable=False, primary_key=True)
    key: UUID = Column(UUID, default=uuid4, nullable=False, primary_key=False)
    name: str = Column(String, default="Loxi", nullable=False)

    members = relationship("Member", back_populates="team")
    # один к одному
    team_statistic_uuid: UUID = Column(UUID, ForeignKey("team_statistic.uuid"), nullable=False, index=True)
