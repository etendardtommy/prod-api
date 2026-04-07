from pydantic import BaseModel
from datetime import datetime


class RosterMemberBase(BaseModel):
    name: str
    number: str | None = None
    role: str | None = None
    photo_url: str | None = None
    eva_url: str | None = None
    published: bool = True
    sort_order: int = 0


class RosterMemberCreate(RosterMemberBase):
    site_id: int = 2


class RosterMemberUpdate(BaseModel):
    name: str | None = None
    number: str | None = None
    role: str | None = None
    photo_url: str | None = None
    eva_url: str | None = None
    published: bool | None = None
    sort_order: int | None = None


class RosterMemberResponse(RosterMemberBase):
    id: int
    site_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RosterMemberPublic(BaseModel):
    id: int
    name: str
    number: str | None = None
    role: str | None = None
    photo_url: str | None = None
    eva_url: str | None = None

    model_config = {"from_attributes": True}
