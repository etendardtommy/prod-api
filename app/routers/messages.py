from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user
from app.models.message import Message
from app.models.user import User
from app.schemas.message import MessageCreate, MessageResponse

router = APIRouter()


# --- Public ---

@router.post("/public", response_model=MessageResponse, status_code=201)
async def send_message(
    data: MessageCreate,
    x_site_id: int = Header(default=1, alias="x-site-id"),
    db: Session = Depends(get_db),
):
    message = Message(site_id=x_site_id, **data.model_dump())
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


# --- Admin ---

@router.get("/", response_model=list[MessageResponse])
async def list_messages(
    site_id: int | None = None,
    is_read: bool | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Message)
    if site_id is not None:
        query = query.filter(Message.site_id == site_id)
    if is_read is not None:
        query = query.filter(Message.is_read == is_read)
    return query.order_by(Message.created_at.desc()).all()


@router.put("/{message_id}/read", response_model=MessageResponse)
async def mark_as_read(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message non trouvé")
    message.is_read = True
    db.commit()
    db.refresh(message)
    return message


@router.delete("/{message_id}", status_code=204)
async def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    message = db.query(Message).filter(Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message non trouvé")
    db.delete(message)
    db.commit()
