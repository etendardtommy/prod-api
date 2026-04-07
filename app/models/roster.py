from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class RosterMember(Base):
    __tablename__ = "roster_members"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, nullable=False, default=2, index=True)
    name = Column(String, nullable=False)
    number = Column(String, nullable=True)
    role = Column(String, nullable=True)
    photo_url = Column(String, nullable=True)
    eva_url = Column(String, nullable=True)
    published = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
