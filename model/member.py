from uuid import uuid4
from sqlalchemy import Column, Integer, String, ForeignKey, UUID, Boolean, CheckConstraint
from .base_class import BaseClass
from sqlalchemy.orm import relationship

class Member(BaseClass):

    __tablename__ = 'member'

    uuid: UUID = Column(UUID, default=uuid4, nullable=False, primary_key=True)

    team_uuid: UUID = Column(UUID, ForeignKey("team.uuid"), nullable=False, index=True)
    team = relationship("Team", back_populates="members")

    role_uuid: UUID = Column(UUID, ForeignKey("role.uuid"), nullable=False, index=True)
    role = relationship("Role", back_populates="members")
