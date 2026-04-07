from pydantic import BaseModel
from datetime import datetime


class ExperienceBase(BaseModel):
    title: str
    company: str
    location: str | None = None
    description: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    technologies: str | None = None
    published: bool = True
    sort_order: int = 0


class ExperienceCreate(ExperienceBase):
    site_id: int = 1


class ExperienceUpdate(BaseModel):
    title: str | None = None
    company: str | None = None
    location: str | None = None
    description: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    technologies: str | None = None
    published: bool | None = None
    sort_order: int | None = None


class ExperienceResponse(ExperienceBase):
    id: int
    site_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ExperiencePublic(BaseModel):
    id: int
    title: str
    company: str
    location: str | None = None
    description: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    technologies: str | None = None

    model_config = {"from_attributes": True}
