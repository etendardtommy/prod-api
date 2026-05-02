from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.match import Match
from app.schemas.match import MatchPublic

router = APIRouter()


@router.get("/public", response_model=list[MatchPublic])
async def get_public_matches(
    x_site_id: int = Header(default=2, alias="x-site-id"),
    db: Session = Depends(get_db),
):
    return (
        db.query(Match)
        .filter(Match.site_id == x_site_id)
        .order_by(Match.scheduled_at.desc().nullslast(), Match.played_at.desc().nullslast())
        .all()
    )
