"""
Script pour créer le premier utilisateur admin.
Usage: python seed.py
"""
import sys
import getpass
import os
from app.database import SessionLocal, engine
from app.models import *  # noqa: F401, F403 — force import de tous les modèles
from app.database import Base
from app.models.user import User
from app.auth import hash_password


def seed():
    email = os.getenv("ADMIN_EMAIL") or input("Email admin : ").strip()
    password = os.getenv("ADMIN_PASSWORD") or getpass.getpass("Mot de passe admin : ")

    if not email or not password:
        print("Erreur : email et mot de passe requis.")
        sys.exit(1)

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        print(f"L'utilisateur {email} existe déjà.")
        db.close()
        return

    admin = User(
        email=email,
        username=email.split("@")[0],
        hashed_password=hash_password(password),
        is_active=True,
        is_superadmin=True,
    )
    db.add(admin)
    db.commit()
    print(f"Utilisateur admin créé : {email}")
    db.close()


if __name__ == "__main__":
    seed()
