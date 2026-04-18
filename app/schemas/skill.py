from pydantic import BaseModel
from datetime import datetime


class SkillBase(BaseModel):
    name: str
    logo_url: str | None = None
    category: str | None = None
    description: str | None = None
    details: str | None = None
    published: bool = True
    sort_order: int = 0


class SkillCreate(SkillBase):
    site_id: int = 1


class SkillUpdate(BaseModel):
    name: str | None = None
    logo_url: str | None = None
    category: str | None = None
    description: str | None = None
    details: str | None = None
    published: bool | None = None
    sort_order: int | None = None


class SkillResponse(SkillBase):
    id: int
    site_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SkillPublic(BaseModel):
    id: int
    name: str
    logo_url: str | None = None
    category: str | None = None
    description: str | None = None
    details: str | None = None
    sort_order: int

    model_config = {"from_attributes": True}
