"""
Script pour créer le premier utilisateur admin.
Usage: python seed.py
"""
import sys
from app.database import SessionLocal, engine
from app.models import *  # noqa: F401, F403 — force import de tous les modèles
from app.database import Base
from app.models.user import User
from app.auth import hash_password


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    existing = db.query(User).filter(User.email == "admin@t-etendard.fr").first()
    if existing:
        print("L'utilisateur admin existe déjà.")
        db.close()
        return

    admin = User(
        email="admin@t-etendard.fr",
        username="admin",
        hashed_password=hash_password("changeme"),
        is_active=True,
        is_superadmin=True,
    )
    db.add(admin)
    db.commit()
    print("Utilisateur admin créé : admin@t-etendard.fr / changeme")
    print("⚠ Change le mot de passe en production !")
    db.close()


if __name__ == "__main__":
    seed()
