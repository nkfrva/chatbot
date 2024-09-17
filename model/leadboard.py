from uuid import uuid4
from sqlalchemy import Column, String, UUID, ForeignKey, Integer
from .base_class import BaseClass


class LeadBoard(BaseClass):

    __tablename__ = 'leadboard'

    uuid: UUID = Column(UUID, default=uuid4, nullable=False, primary_key=True)
    team_uuid: UUID = Column(UUID, ForeignKey("team.uuid"), nullable=False, index=True)
    points: int = Column(Integer, default=0, nullable=False)
    passage_time: str = Column(String, default="00:00:00", nullable=False)
