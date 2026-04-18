from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, nullable=False, default=1, index=True)
    name = Column(String, nullable=False)
    logo_url = Column(String, nullable=True)
    category = Column(String, nullable=True)  # tags séparés par virgule
    description = Column(String, nullable=True)
    details = Column(Text, nullable=True)
    published = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
