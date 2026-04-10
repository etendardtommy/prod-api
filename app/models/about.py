from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base


class About(Base):
    __tablename__ = "about"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, nullable=False, default=1, index=True)
    photo_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)          # markdown
    github_url = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    cv_url = Column(String, nullable=True)
    published = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
