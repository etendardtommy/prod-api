from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, nullable=False, index=True)
    eva_match_id = Column(String, unique=True, nullable=False, index=True)
    tournament_id = Column(String, nullable=False)
    tournament_name = Column(String, nullable=False)
    division = Column(String, nullable=True)
    opponent_name = Column(String, nullable=False)
    opponent_logo_url = Column(String, nullable=True)
    scheduled_at = Column(DateTime(timezone=True), nullable=True)
    played_at = Column(DateTime(timezone=True), nullable=True)
    status = Column(String, nullable=False, default="pending")  # pending, running, completed
    score_eclyps = Column(Integer, nullable=True)
    score_opponent = Column(Integer, nullable=True)
    result = Column(String, nullable=True)  # win, loss, draw
    synced_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
