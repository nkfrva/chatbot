from uuid import uuid4
from sqlalchemy import Column, String, ForeignKey, UUID, Boolean
from .base_class import BaseClass
from sqlalchemy.orm import relationship


class Member(BaseClass):

    __tablename__ = 'member'

    uuid: UUID = Column(UUID, default=uuid4, nullable=False, primary_key=True)
    team_uuid: UUID = Column(UUID, ForeignKey("team.uuid"), nullable=False, index=True)
    user_id: str = Column(String, default="111", nullable=False)
    username: str = Column(String, default="111", nullable=False)
    ban: bool = Column(Boolean, default=False, nullable=False)

    teams = relationship("Team", back_populates="members")

