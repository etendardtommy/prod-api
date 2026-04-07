from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models.experience import Experience
from app.models.user import User
from app.schemas.experience import (
    ExperienceCreate,
    ExperienceUpdate,
    ExperienceResponse,
    ExperiencePublic,
)

router = APIRouter()


# --- Public ---

@router.get("/public", response_model=list[ExperiencePublic])
async def get_public_experiences(db: Session = Depends(get_db)):
    return (
        db.query(Experience)
        .filter(Experience.published == True, Experience.site_id == 1)
        .order_by(Experience.sort_order)
        .all()
    )


# --- Admin ---

@router.get("/", response_model=list[ExperienceResponse])
async def list_experiences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Experience).order_by(Experience.sort_order).all()


@router.post("/", response_model=ExperienceResponse, status_code=201)
async def create_experience(
    data: ExperienceCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exp = Experience(**data.model_dump())
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp


@router.put("/{exp_id}", response_model=ExperienceResponse)
async def update_experience(
    exp_id: int,
    data: ExperienceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exp = db.query(Experience).filter(Experience.id == exp_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Expérience non trouvée")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(exp, key, value)
    db.commit()
    db.refresh(exp)
    return exp


@router.delete("/{exp_id}", status_code=204)
async def delete_experience(
    exp_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exp = db.query(Experience).filter(Experience.id == exp_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Expérience non trouvée")
    db.delete(exp)
    db.commit()
