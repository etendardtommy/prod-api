from pydantic import BaseModel
from datetime import datetime


class MatchPublic(BaseModel):
    id: int
    eva_match_id: str
    tournament_name: str
    division: str | None = None
    opponent_name: str
    opponent_logo_url: str | None = None
    scheduled_at: datetime | None = None
    played_at: datetime | None = None
    status: str
    score_eclyps: int | None = None
    score_opponent: int | None = None
    result: str | None = None

    model_config = {"from_attributes": True}
