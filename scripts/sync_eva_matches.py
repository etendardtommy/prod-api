"""
Sync ECLYPS matches from competitive.eva.gg into the local database.
Run manually or via systemd timer (every 6h).

Usage: uv run python scripts/sync_eva_matches.py
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from datetime import datetime, timezone
from app.database import SessionLocal
from app.models.match import Match

EVA_API = "https://competitive.eva.gg/api"
ECLYPS_TEAM_ID = "2448652881169059839"
SITE_ID = 2


def eva_get(path, params=None, range_header=None):
    headers = {}
    if range_header:
        headers["Range"] = range_header
    r = requests.get(f"{EVA_API}{path}", params=params, headers=headers, timeout=15)
    r.raise_for_status()
    return r.json()


def parse_dt(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def sync():
    db = SessionLocal()
    synced = 0
    errors = 0

    try:
        # 1. Find all tournament registrations for ECLYPS
        participants = eva_get(
            "/participants",
            params={"team_id": ECLYPS_TEAM_ID},
            range_header="participants=0-49",
        )

        if not participants:
            print("Aucune participation trouvée pour ECLYPS.")
            return

        for participant in participants:
            participant_id = str(participant.get("id", ""))
            tournament = participant.get("tournament", {})
            tournament_id = str(tournament.get("id", ""))
            tournament_name = tournament.get("name") or "JARL League"

            if not participant_id or not tournament_id:
                continue

            # 2. Fetch matches for this participant
            try:
                matches = eva_get(
                    "/matches",
                    params={"participant_ids": participant_id},
                    range_header="matches=0-99",
                )
            except Exception as e:
                print(f"Erreur fetch matchs pour participant {participant_id}: {e}")
                errors += 1
                continue

            for match in matches:
                try:
                    eva_match_id = str(match.get("id", ""))
                    if not eva_match_id:
                        continue

                    opponents = match.get("opponents", [])
                    eclyps_opp = None
                    other_opp = None

                    for opp in opponents:
                        p = opp.get("participant", {})
                        if str(p.get("id", "")) == participant_id:
                            eclyps_opp = opp
                        else:
                            other_opp = opp

                    if not other_opp:
                        continue

                    opponent_name = (
                        other_opp.get("participant", {}).get("name")
                        or other_opp.get("participant", {}).get("team", {}).get("name")
                        or "Adversaire inconnu"
                    )
                    opponent_logo_url = (
                        other_opp.get("participant", {}).get("logoUrl")
                        or other_opp.get("participant", {}).get("team", {}).get("logoUrl")
                    )

                    score_eclyps = eclyps_opp.get("score") if eclyps_opp else None
                    score_opponent = other_opp.get("score")

                    result_raw = eclyps_opp.get("result") if eclyps_opp else None
                    if result_raw == "win":
                        result = "win"
                    elif result_raw == "loss":
                        result = "loss"
                    elif result_raw == "draw":
                        result = "draw"
                    else:
                        result = None

                    status = match.get("status", "pending")
                    scheduled_at = parse_dt(match.get("scheduledAt"))
                    played_at = parse_dt(match.get("playedAt"))

                    division = None
                    stage = match.get("stage") or {}
                    if stage.get("name"):
                        division = stage["name"]

                    # Upsert
                    existing = db.query(Match).filter(Match.eva_match_id == eva_match_id).first()
                    if existing:
                        existing.tournament_name = tournament_name
                        existing.division = division
                        existing.opponent_name = opponent_name
                        existing.opponent_logo_url = opponent_logo_url
                        existing.scheduled_at = scheduled_at
                        existing.played_at = played_at
                        existing.status = status
                        existing.score_eclyps = score_eclyps
                        existing.score_opponent = score_opponent
                        existing.result = result
                        existing.synced_at = datetime.now(timezone.utc)
                    else:
                        db.add(Match(
                            site_id=SITE_ID,
                            eva_match_id=eva_match_id,
                            tournament_id=tournament_id,
                            tournament_name=tournament_name,
                            division=division,
                            opponent_name=opponent_name,
                            opponent_logo_url=opponent_logo_url,
                            scheduled_at=scheduled_at,
                            played_at=played_at,
                            status=status,
                            score_eclyps=score_eclyps,
                            score_opponent=score_opponent,
                            result=result,
                        ))

                    db.commit()
                    synced += 1

                except Exception as e:
                    db.rollback()
                    print(f"Erreur match {match.get('id')}: {e}")
                    errors += 1

    finally:
        db.close()

    print(f"Sync terminé — {synced} matchs traités, {errors} erreurs.")


if __name__ == "__main__":
    sync()
