from pydantic import BaseModel
from datetime import datetime


class MessageCreate(BaseModel):
    name: str
    email: str
    subject: str | None = None
    content: str


class MessageResponse(BaseModel):
    id: int
    site_id: int
    name: str
    email: str
    subject: str | None = None
    content: str
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}
