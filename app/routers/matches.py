import json
import urllib.request
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.match import Match
from app.schemas.match import MatchPublic

router = APIRouter()

EVA_API = "https://competitive.eva.gg/api"
UA = "Mozilla/5.0 (compatible; ECLYPS-sync/1.0)"


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
async def get_standings(
    x_site_id: int = Header(default=2, alias="x-site-id"),
    db: Session = Depends(get_db),
):
    # Trouve le tournoi le plus récent avec des matchs joués
    last_match = (
        db.query(Match)
        .filter(Match.site_id == x_site_id, Match.status == "completed")
        .order_by(Match.played_at.desc().nullslast())
        .first()
    )
    if not last_match:
        return []

    tournament_id = last_match.tournament_id
    tournament_name = last_match.tournament_name

    # Récupère tous les matchs du tournoi depuis l'API EVA
    try:
        req = urllib.request.Request(
            f"{EVA_API}/matches?tournament_ids={tournament_id}",
            headers={"User-Agent": UA, "Accept": "application/json"},
        )
        req.add_header("Range", "matches=0-99")
        with urllib.request.urlopen(req, timeout=10) as r:
            all_matches = json.loads(r.read())
    except Exception:
        raise HTTPException(status_code=502, detail="Impossible de contacter l'API EVA")

    # Calcule le classement
    teams: dict[str, dict] = {}
    for m in all_matches:
        if m.get("status") != "completed":
            continue
        for opp in m.get("opponents", []):
            p = opp.get("participant", {})
            name = p.get("name") or "?"
            logo_fields = p.get("customFieldValues", {}).get("logo", {})
            logo = logo_fields.get("logo_medium") or logo_fields.get("icon_medium")
            result = opp.get("result")

            if name not in teams:
                teams[name] = {"name": name, "logo": logo, "wins": 0, "losses": 0, "draws": 0, "points": 0, "played": 0}
            teams[name]["played"] += 1
            if result == "win":
                teams[name]["wins"] += 1
                teams[name]["points"] += 3
            elif result == "loss":
                teams[name]["losses"] += 1
            elif result == "draw":
                teams[name]["draws"] += 1
                teams[name]["points"] += 1

    ranking = sorted(teams.values(), key=lambda t: (-t["points"], -t["wins"]))
    for i, team in enumerate(ranking, 1):
        team["rank"] = i

    return {"tournament_name": tournament_name, "standings": ranking}
