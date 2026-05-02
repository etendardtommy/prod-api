import json
import urllib.request
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.match import Match
from app.schemas.match import MatchPublic

router = APIRouter()

EVA_API = "https://competitive.eva.gg/api"
EVA_MEDIA = "https://competitive.eva.gg/media/file"
UA = "Mozilla/5.0 (compatible; ECLYPS-sync/1.0)"

JARL_RANKING_ID = "2441507312469446655"


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


@router.get("/standings")
async def get_standings():
    try:
        req = urllib.request.Request(
            f"{EVA_API}/circuit-ranking-items?ranking_ids={JARL_RANKING_ID}",
            headers={"User-Agent": UA, "Accept": "application/json"},
        )
        req.add_header("Range", "items=0-49")
        with urllib.request.urlopen(req, timeout=10) as r:
            items = json.loads(r.read())
    except Exception:
        raise HTTPException(status_code=502, detail="Impossible de contacter l'API EVA")

    if not items:
        return []

    tournament_name = items[0]["ranking"]["name"]
    standings = []
    for item in items:
        entity = item.get("entity") or {}
        logo_obj = entity.get("logo") or {}
        logo_id = logo_obj.get("id") if isinstance(logo_obj, dict) else None
        logo_url = f"{EVA_MEDIA}/{logo_id}/logo_medium" if logo_id else None
        props = item.get("properties") or {}
        standings.append({
            "rank": item["rank"],
            "position": item["position"],
            "name": entity.get("name", "?"),
            "logo": logo_url,
            "points": item["points"],
            "played": props.get("played", 0),
        })

    return {"tournament_name": tournament_name, "standings": standings}
